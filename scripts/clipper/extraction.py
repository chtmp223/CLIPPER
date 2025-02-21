# Extracting claims from multiple chapter in the story
import sys

sys.path.append("../")
from utils import *
from tqdm import tqdm, trange
import pandas as pd
import traceback
import argparse
import os


def multiple_init(outlines):
    """
    Extracts claims from multiple chapters in the story (initial chapter)
    """
    all_events = []
    for i, out in enumerate(outlines):
        event = (
            f"## Chapter {i+1} outline\n"
            + extract_tag_text(out, "events", random=False).strip()
        )
        all_events.append(event)
    event_text = "\n\n".join(all_events)

    to_prompt = open("../../prompts/extraction_multiple.md", "r").read()
    prompt = to_prompt.format(chapter_outlines=event_text)
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
    )

    # Processing the responses
    if "<facts>" not in responses:
        print(responses)
        return pd.DataFrame(
            {
                "facts": [],
                "explanation": [],
                "source": [],
                "brainstorm": [],
                "corrupted": [],
                "corrupted_reasoning": [],
            }
        )
    if "</facts>" not in responses:
        responses += "</facts>"
    claims = extract_tag_text(responses, "facts", random=False).strip()
    claim_exp, claim_text, source, brainstorms, corrupted, corrupted_reasoning = (
        [],
        [],
        [],
        [],
        [],
        [],
    )
    num_claims = len(re.findall(r"<fact_(\d+)>", claims))
    for i in range(num_claims):
        try:
            # Inserting closing tags if missing
            if f"</fact_{i+1}>" not in claims:
                if f"<fact_{i+2}>" in claims:
                    claims = claims.replace(
                        f"<fact_{i+2}>", f"</fact_{i+1}>\n\n<fact_{i+2}>"
                    )
                else:
                    claims += f"</fact_{i+1}>"
            c = extract_tag_text(claims, f"fact_{i+1}", random=False)
            if "<brainstorm>" not in c:  # No meaningful fact
                continue
            brainstorm = extract_tag_text(c, "brainstorm", random=False)
            c = c.replace(f"<brainstorm>{brainstorm}</brainstorm>", "").strip()
            if ":" in c and len(c.split("\n")) == 5:
                brainstorms.append(brainstorm.strip())
                claim_text.append(": ".join(c.split("\n")[0].split(": ")[1:]))
                claim_exp.append(": ".join(c.split("\n")[1].split(": ")[1:]))
                source.append(": ".join(c.split("\n")[2].split(": ")[1:]))
                corrupted.append(": ".join(c.split("\n")[3].split(": ")[1:]))
                corrupted_reasoning.append(": ".join(c.split("\n")[4].split(": ")[1:]))
            else:
                print("Invalid claim (likely missing corruption)")
                continue
        except Exception as e:
            traceback.print_exc()
            print(claims)
            print("Failed to extract fact {}".format(i + 1))

    df = pd.DataFrame(
        {
            "facts": claim_text,
            "corrupted_facts": corrupted,
            "fact_reasoning": claim_exp,
            "corrupted_reasoning": corrupted_reasoning,
            "source": source,
            "brainstorm": brainstorms,
        }
    )
    print(f"Length of df after the first iteration: {len(df)}")
    return df


def multiple_cont(existing_df, outlines, times=10):
    """
    Continues extracting claims from multiple chapters in the story (continuing from the initial chapters)
    """
    all_claims = []
    df = existing_df.copy()

    # Replace the chapter outline with only the events
    all_events = []
    for i, out in enumerate(outlines):
        event = (
            f"## Chapter {i+1} outline\n"
            + extract_tag_text(out, "events", random=False).strip()
        )
        all_events.append(event)
    event_text = "\n\n".join(all_events)

    for time in trange(times):
        # Combine existing claims
        prompt = open("../../prompts/extraction_multiple_cont.md", "r").read()
        if len(all_claims) == 0:
            existing = existing_df["facts"].tolist()
        else:
            existing = existing_df["facts"].tolist() + all_claims
        existing_claims = "\n".join(
            [f"- Fact {i+1}: {fact}" for i, fact in enumerate(existing)]
        )

        prompt = prompt.format(
            chapter_outlines=event_text, existing_facts=existing_claims
        )
        responses = prompt_claude(
            prompt,
            verbose=False,
            metadata={
                "model": "claude-3-5-sonnet@20240620",
                "temp": 0.0,
                "max_tokens": 4096,
                "top_p": 1.0,
            },
            system_message="You are an expert at extracting facts from fictional narratives.",
        )
        if "<facts>" not in responses:
            print(responses)
            return pd.DataFrame(
                {
                    "facts": [],
                    "explanation": [],
                    "source": [],
                    "brainstorm": [],
                    "corrupted": [],
                    "corrupted_reasoning": [],
                }
            )
        if "</facts>" not in responses:
            responses += "</facts>"
        try:
            claims = extract_tag_text(responses, "facts", random=False).strip()
        except Exception as e:
            print(responses)
            print("No meaningful claims found")
            continue
        claim_exp, claim_text, source, brainstorms = [], [], [], []
        corrupted, corrupted_reasoning = [], []
        num_claims = len(re.findall(r"<fact_(\d+)>", claims))
        if num_claims == 0:
            print("No claims found")
            return df
        for i in range(num_claims):
            try:
                if f"</fact_{i+1}>" not in claims:
                    if f"<fact_{i+2}>" in claims:
                        claims = claims.replace(
                            f"<fact_{i+2}>", f"</fact_{i+1}>\n\n<fact_{i+2}>"
                        )
                    else:
                        claims += f"</fact_{i+1}>"
                c = extract_tag_text(claims, f"fact_{i+1}", random=False)
                if "<brainstorm>" not in c:  # No meaningful fact
                    continue
                brainstorm = extract_tag_text(c, "brainstorm", random=False)
                c = c.replace(f"<brainstorm>{brainstorm}</brainstorm>", "").strip()
                if ":" in c and len(c.split("\n")) == 5:
                    brainstorms.append(brainstorm.strip())
                    claim_text.append(": ".join(c.split("\n")[0].split(": ")[1:]))
                    claim_exp.append(": ".join(c.split("\n")[1].split(": ")[1:]))
                    source.append(": ".join(c.split("\n")[2].split(": ")[1:]))
                    corrupted.append(": ".join(c.split("\n")[3].split(": ")[1:]))
                    corrupted_reasoning.append(
                        ": ".join(c.split("\n")[4].split(": ")[1:])
                    )
                else:
                    print("Invalid claim (likely missing corruption)")
                    continue
            except Exception as e:
                traceback.print_exc()
                print(claims)
                print("Failed to extract fact {}".format(i + 1))

        df = pd.DataFrame(
            {
                "facts": claim_text,
                "corrupted_facts": corrupted,
                "fact_reasoning": claim_exp,
                "corrupted_reasoning": corrupted_reasoning,
                "source": source,
                "brainstorm": brainstorms,
            }
        )
        df = pd.concat([existing_df, df])
        print(f"Length of df after {time+2} iterations: {len(df)}")
        existing_df = df.copy()
    return df


def single(outlines, existing_df, book_name):
    """
    Extracting claims from a single chapter in the story
    """
    summary = open(f"../../data/output/{book_name}/summary.md", "r").read()
    existing_facts_list = existing_df["facts"].apply(lambda x: x.strip()).tolist()
    p = open("../../prompts/extraction_single.md", "r").read()

    claim_text, claim_exp, source, brainstorms = [], [], [], []
    corrupted, corrupted_reasoning = [], []
    for i, chap in enumerate(tqdm(outlines)):
        existing = "\n".join(
            [f"- Fact {i+1}: {fact}" for i, fact in enumerate(existing_facts_list)]
        )
        prompt = p.format(
            book_summary=summary,
            chapter_outline=f"## Chapter {i+1} outline\n"
            + extract_tag_text(chap, "events", random=False).strip(),
            existing_facts=existing,
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
            system_message="You are an expert at extracting facts from fictional narratives.",
        )
        if "<facts>" not in response:
            print(response)
            return pd.DataFrame(
                {
                    "facts": [],
                    "explanation": [],
                    "source": [],
                    "brainstorm": [],
                    "corrupted": [],
                    "corrupted_reasoning": [],
                }
            )
        if "</facts>" not in response:
            response += "</facts>"
        claims = extract_tag_text(response, "facts", random=False).strip()
        num_claims = len(re.findall(r"<fact_(\d+)>", claims))
        for i in range(num_claims):
            try:
                if f"</fact_{i+1}>" not in claims:
                    if f"<fact_{i+2}>" in claims:
                        claims = claims.replace(
                            f"<fact_{i+2}>", f"</fact_{i+1}>\n\n<fact_{i+2}>"
                        )
                    else:
                        claims += f"</fact_{i+1}>"
                c = extract_tag_text(claims, f"fact_{i+1}", random=False)
                if "<brainstorm>" not in c:  # No meaningful fact
                    continue
                brainstorm = extract_tag_text(c, "brainstorm", random=False)
                c = c.replace(f"<brainstorm>{brainstorm}</brainstorm>", "").strip()
                if ":" in c and len(c.split("\n")) == 5:
                    brainstorms.append(brainstorm.strip())
                    claim_text.append(": ".join(c.split("\n")[0].split(": ")[1:]))
                    claim_exp.append(": ".join(c.split("\n")[1].split(": ")[1:]))
                    source.append(": ".join(c.split("\n")[2].split(": ")[1:]))
                    corrupted.append(": ".join(c.split("\n")[3].split(": ")[1:]))
                    corrupted_reasoning.append(
                        ": ".join(c.split("\n")[4].split(": ")[1:])
                    )
                else:
                    print("Invalid claim (likely missing corruption)")
                    continue
            except Exception as e:
                traceback.print_exc()
                print(claims)
                print("Failed to extract fact {}".format(i + 1))

    df = pd.DataFrame(
        {
            "facts": claim_text,
            "corrupted_facts": corrupted,
            "fact_reasoning": claim_exp,
            "corrupted_reasoning": corrupted_reasoning,
            "source": source,
            "brainstorm": brainstorms,
        }
    )
    print(f"Length of df after single chapter extraction: {len(df)}")
    return df


def extraction_main(book_name, iteration, gen_type):
    outlines = (
        open(f"../../data/output/{book_name}/outline.md", "r")
        .read()
        .split("\n----------------\n")
    )

    if gen_type.lower().strip() in ["multiple", "both"]:
        os.makedirs(f"../../data/output/{book_name}/claims", exist_ok=True)
        df = multiple_init(outlines)
        df.to_csv(
            f"../../data/output/{book_name}/claims/claims_multiple_raw.csv", index=False
        )
        cont_df = multiple_cont(df, outlines, times=int(iteration))
        cont_df.to_csv(
            f"../../data/output/{book_name}/claims/claims_multiple_raw.csv", index=False
        )
    if gen_type.lower().strip() in ["single", "both"]:
        cont_df = pd.read_csv(
            f"../../data/output/{book_name}/claims/claims_multiple_raw.csv"
        )
        single_df = single(outlines, cont_df, book_name)
        single_df.to_csv(
            f"../../data/output/{book_name}/claims/claims_single_raw.csv", index=False
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--book_name", help="Name of the book")
    parser.add_argument(
        "--iteration",
        help="Number of times to continue extracting claims from multiple chapters",
        default=10,
    )
    parser.add_argument("--gen_type", help="single, multiple, or both", required=True)
    args = parser.parse_args()
    book_name = args.book_name
    iteration = args.iteration
    gen_type = args.gen_type

    extraction_main(book_name, iteration, gen_type)
