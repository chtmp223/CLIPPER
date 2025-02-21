import sys

sys.path.append("../")
from utils import *
from tqdm import tqdm, trange
import pandas as pd
import traceback
import argparse
import os
import re


def extraction(story, story_id):
    """
    Extracts claims from the story text (no compression)
    Return a dataframe, where each row is an extracted claim.
    """
    # Prompting API to get a list of generated claims
    to_prompt = open("../../prompts/extraction_wp.md", "r").read()
    prompt = to_prompt.format(story=story)
    responses = prompt_claude(
        prompt,
        verbose=True,
        metadata={
            "model": "claude-3-5-sonnet@20240620",
            "temp": 0.0,
            "max_tokens": 4096,
            "top_p": 1.0,
        },
        system_message="You are an expert at extracting facts from fictional narratives.",
        project_id="",  # TODO: specify vertex project id
    )

    # Extracting the generated claims from the responses
    if "<facts>" not in responses:
        return pd.DataFrame(
            {
                "facts": [],
                "explanation": [],
                "source": [],
                "brainstorm": [],
                "corrupted": [],
                "corrupted_reasoning": [],
                "story": [],
                "id": [],
            }
        )

    claim_exp, claim_text, source = [], [], []
    brainstorms, corrupted, corrupted_reasoning = [], [], []

    claims_text = extract_tag_text(responses, "facts", random=False).strip()
    num_claims = len(re.findall(r"<fact_(\d+)>", claims_text))

    for i in range(num_claims):
        try:
            # Insert closing tags if missing
            if f"</fact_{i+1}>" not in claims_text:
                if f"<fact_{i+2}>" in claims_text:
                    claims_text = claims_text.replace(
                        f"<fact_{i+2}>", f"</fact_{i+1}>\n\n<fact_{i+2}>"
                    )
                else:
                    claims_text += f"</fact_{i+1}>"
            c = extract_tag_text(claims_text, f"fact_{i+1}", random=False)
            if "<brainstorm>" not in c:  # No meaningful fact
                continue
            # Extract the brainstorm block
            brainstorm = extract_tag_text(c, "brainstorm", random=False)
            c = c.replace(f"<brainstorm>{brainstorm}</brainstorm>", "").strip()

            if ":" in c and len(c.split("\n")) == 5:
                brainstorms.append(brainstorm.strip())
                claim_text.append(": ".join(c.split("\n")[0].split(": ")[1:]))
                claim_exp.append(": ".join(c.split("\n")[1].split(": ")[1:]))
                source.append("Current story")
                corrupted.append(": ".join(c.split("\n")[3].split(": ")[1:]))
                corrupted_reasoning.append(": ".join(c.split("\n")[4].split(": ")[1:]))
            else:
                print("Invalid claim (likely missing corruption)")
                continue
        except Exception as e:
            traceback.print_exc()
            print(claims_text)
            print(f"Failed to extract fact {i+1}")

    df = pd.DataFrame(
        {
            "facts": claim_text,
            "corrupted_facts": corrupted,
            "fact_reasoning": claim_exp,
            "corrupted_reasoning": corrupted_reasoning,
            "source": source,
            "brainstorm": brainstorms,
            "story": [story for _ in range(len(claim_text))],
            "id": [story_id for _ in range(len(claim_text))],
        }
    )
    return df


def wp(num_desired_claims):
    # I/O path
    input_path = f"../../data/wp/wp.csv"
    output_path = f"../../data/wp/wp_claims.csv"
    df_input = pd.read_csv(input_path)

    # If the output file does not exist or is empty, create it with headers
    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        pd.DataFrame(
            columns=[
                "facts",
                "corrupted_facts",
                "fact_reasoning",
                "corrupted_reasoning",
                "source",
                "brainstorm",
                "story",
                "id",
                "duplication",
                "duplication_reasoning",
            ]
        ).to_csv(output_path, index=False)
        output_dfs = pd.DataFrame()
    else:
        output_dfs = pd.read_csv(output_path)
        output_dfs = output_dfs.drop_duplicates(subset=["facts"]).reset_index(drop=True)
        output_dfs = output_dfs.drop_duplicates(subset=["corrupted_facts"]).reset_index(
            drop=True
        )
        output_dfs = output_dfs[
            ~(output_dfs["duplication"] == "Duplicate")
        ].reset_index(drop=True)
        if len(output_dfs) >= num_desired_claims:
            print(f"Reached {num_desired_claims} claims. Stopping extraction.")
            return

    # Continue processing from the most recent ID if the file is not empty
    already_processed = max([int(s) for s in output_dfs["id"].tolist()])
    print(f"Largest id being processed: {already_processed}")
    df_input = df_input[df_input["id"].astype(int) > already_processed].reset_index(
        drop=True
    )

    # Prepare the story texts and IDs
    stories = df_input["text"].tolist()
    story_ids = df_input["id"].tolist()

    for i, story in enumerate(tqdm(stories)):
        output_dfs = output_dfs.drop_duplicates(subset=["facts"]).reset_index(drop=True)
        output_dfs = output_dfs.drop_duplicates(subset=["corrupted_facts"]).reset_index(
            drop=True
        )
        output_dfs = output_dfs[
            ~(output_dfs["duplication"] == "Duplicate")
        ].reset_index(drop=True)
        print(f"Length after {i} iterations:", len(output_dfs))
        if len(output_dfs) >= num_desired_claims:
            print(f"Reached {num_desired_claims} claims. Stopping extraction.")
            return

        story_id = story_ids[i]
        df_full = extraction(story, story_id)
        print(f"Extracted {len(df_full)} claims from story {i+1}")

        # --- Deduplicate claims ---
        all_claims = df_full["facts"].tolist()
        claim_list = [f"{idx+1}. {c}" for idx, c in enumerate(all_claims)]
        prompt = (
            open("../../prompts/duplication.md", "r")
            .read()
            .format(fact_list="\n".join(claim_list))
        )
        response = prompt_claude(
            prompt,
            verbose=False,
            metadata={
                "model": "claude-3-5-sonnet@20240620",
                "temp": 0.0,
                "max_tokens": 4096,
                "top_p": 1.0,
            },
            system_message="You are an expert at identifying duplicate claims.",
            project_id="",  # TODO
        )

        # If no meaningful duplicate info is returned
        if "<answer>" not in response and not re.search(r"\d", response):
            df_full["duplication"] = ["Unique" for _ in range(len(all_claims))]
            df_full["duplication_reasoning"] = [
                "Unique claim" for _ in range(len(all_claims))
            ]
            print("No duplicates found")
        else:
            try:
                answer = extract_tag_text(response, "answer", random=False).strip()
                answers = [
                    re.sub(r"^\- ", "", a) for a in answer.split("\n") if len(a) > 0
                ]
            except:
                answers = []
            if len(answers) == 0:
                df_full["duplication"] = ["Unique" for _ in range(len(all_claims))]
                df_full["duplication_reasoning"] = [
                    "Unique claim" for _ in range(len(all_claims))
                ]
                print("No duplicates found")
            else:
                # Parse duplicates
                all_dups = []
                for a in answers:
                    # Each line might look like: 2, 5: Duplicates of claim #1
                    split_line = a.split(": ")
                    if len(split_line) < 2:
                        continue
                    try:
                        duplicates_str, reasoning = split_line[0], " ".join(
                            split_line[1:]
                        )
                    except:
                        print(f"ERROR: {split_line}")
                        sys.exit()
                    # grab the indices before the colon
                    dup_index = [
                        int(item)
                        for item in duplicates_str.split(", ")
                        if item.isnumeric()
                    ]
                    all_dups.append(dup_index)

                all_dups_flat = [item for sublist in all_dups for item in sublist]
                first_ind = [lst[0] for lst in all_dups if len(lst) > 0]
                dups_flat = list(set(all_dups_flat) - set(first_ind))

                explanations = {}
                for a in answers:
                    if ": " not in a:
                        continue
                    left_side, exp = a.split(": ", 1)
                    claims = [
                        item for item in left_side.split(", ") if item.isnumeric()
                    ]
                    for c in claims:
                        explanations[c] = exp

                # Mark each claim
                dup_final, dup_exp = [], []
                for idx in range(len(all_claims)):
                    if (idx + 1) in dups_flat:
                        dup_final.append("Duplicate")
                        dup_exp.append(
                            explanations.get(str(idx + 1), "Likely duplicate")
                        )
                    else:
                        dup_final.append("Unique")
                        dup_exp.append("Valid claim")

                df_full["duplication"] = dup_final
                df_full["duplication_reasoning"] = dup_exp
                print(
                    f"Identified {len(dups_flat)} duplicate claims out of {len(all_claims)}."
                )

        df_full = df_full.drop_duplicates(
            subset=["facts", "corrupted_facts"]
        ).reset_index(drop=True)
        df_full = df_full[~(df_full["duplication"] == "Duplicate")].reset_index(
            drop=True
        )
        df_full.to_csv(
            output_path, index=False, header=False, mode="a", encoding="utf-8"
        )
        output_dfs = pd.concat([output_dfs, df_full], ignore_index=True)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num_claims",
        help="Total number of claims that you want to extract.",
        default=20000,
        type=int,
    )
    args = parser.parse_args()
    wp(args.num_claims)
