import sys

sys.path.append("../")
from utils import *
import pandas as pd
from tqdm import trange, tqdm
import re
import argparse
import traceback


def verify_claims_iterative(df, book_name):
    """
    Verify whether the claims are valid or not
    """
    p = open("../../prompts/verification.md", "r").read()
    summary = open(f"../../data/output/{book_name}/summary.md", "r").read()
    outline = (
        open(f"../../data/output/{book_name}/outline.md", "r")
        .read()
        .split("\n----------------\n")
    )
    claims = df.facts.tolist()
    source = df.source.tolist()

    verification = []
    reasoning = []
    for i, claim in enumerate(tqdm(claims)):
        if type(source[i]) != str:
            sources = [i for i in range(len(outline))]
        else:
            source_text = source[i]
            if "(" in source_text:
                source_text = source_text.split(" (")[0]
            sources = [int(item) - 1 for item in re.findall(r"(\d+)", source_text)]

        all_source = [
            f"## Chapter {s+1} outline\n"
            + extract_tag_text(outline[s], "events", random=False).strip()
            for s in sources
        ]
        source_text = "\n\n".join(all_source)
        prompt = p.format(
            book_summary=summary, claim=claim, chapter_outline=source_text
        )

        response = prompt_openai(
            prompt,
            verbose=False,
            metadata={
                "model": "gpt-4o-2024-08-06",
                "temp": 0.0,
                "top_p": 1.0,
                "max_tokens": 1000,
            },
            system_message="You are an expert at verifying claims from fictional narratives.",
        )
        try:
            verification.append(
                extract_tag_text(response, "result", random=False).strip()
            )
            reasoning.append(
                extract_tag_text(response, "reasoning", random=False).strip()
            )
        except:
            print(response)
            raise ValueError("Failed to extract verification")

    df["verify_facts"] = verification
    df["verify_facts_reasoning"] = reasoning

    df_failed = df[df["verify_facts"] == "INVALID"]
    print(f"Identified {len(df_failed)} invalid claims")
    return df


def verify_corruption_iterative(df, book_name):
    """
    Verify whether the claims are valid or not
    """
    p = open("../../prompts/verification.md", "r").read()
    summary = open(f"../../data/output/{book_name}/summary.md", "r").read()
    outline = (
        open(f"../../data/output/{book_name}/outline.md", "r")
        .read()
        .split("\n----------------\n")
    )
    claims = df.corrupted_facts.tolist()
    source = df.source.tolist()

    verification = []
    reasoning = []
    for i, claim in enumerate(tqdm(claims)):
        if type(source[i]) != str:
            sources = [i for i in range(len(outline))]
        else:
            source_text = source[i]
            if "(" in source_text:
                source_text = source_text.split(" (")[0]
            sources = [int(item) - 1 for item in re.findall(r"(\d+)", source_text)]

        all_source = [
            f"## Chapter {s+1} outline\n"
            + extract_tag_text(outline[s], "events", random=False).strip()
            for s in sources
        ]
        source_text = "\n\n".join(all_source)
        prompt = p.format(
            book_summary=summary, claim=claim, chapter_outline=source_text
        )
        response = prompt_openai(
            prompt,
            verbose=False,
            metadata={
                "model": "gpt-4o-2024-08-06",
                "temp": 0.0,
                "top_p": 1.0,
                "max_tokens": 1000,
            },
            system_message="You are an expert at verifying claims from fictional narratives.",
        )

        try:
            verification.append(
                extract_tag_text(response, "result", random=False).strip()
            )
            reasoning.append(
                extract_tag_text(response, "reasoning", random=False).strip()
            )
        except:
            print(response)
            raise ValueError("Failed to extract verification")

    df["verify_corruption"] = verification
    df["verify_corruption_reasoning"] = reasoning

    df_failed = df[df["verify_corruption"] == "VALID"]
    print(f"Identified {len(df_failed)} invalid claims")
    return df


def verify_claims(df, book_name):
    """
    Verify whether the claims are valid or not
    """
    p = open("../../prompts/verification.md", "r").read()
    summary = open(f"../../data/output/{book_name}/summary.md", "r").read()
    outline = (
        open(f"../../data/output/{book_name}/outline.md", "r")
        .read()
        .split("\n----------------\n")
    )
    claims = df.facts.tolist()
    source = df.source.tolist()

    verification = []
    reasoning = []
    prompts = []
    for i, claim in enumerate(tqdm(claims)):
        if type(source[i]) != str:
            sources = [i for i in range(len(outline))]
        else:
            source_text = source[i]
            if "(" in source_text:
                source_text = source_text.split(" (")[0]
            sources = [int(item) - 1 for item in re.findall(r"(\d+)", source_text)]

        all_source = [
            f"## Chapter {s+1} outline\n"
            + extract_tag_text(outline[s], "events", random=False).strip()
            for s in sources
        ]
        source_text = "\n\n".join(all_source)
        prompts.append(
            p.format(book_summary=summary, claim=claim, chapter_outline=source_text)
        )

    df_response = format_batch_openai(
        prompts,
        "../../data/batch/verification_in.jsonl",
        "../../data/batch/verification_out.jsonl",
        metadata={
            "model": "gpt-4o-2024-08-06",
            "max_tokens": 1000,
            "temp": 0.0,
            "top_p": 1.0,
            "system_message": "You are an expert at verifying claims from fictional narratives.",
        },
    )
    responses = df_response.response.apply(extract_batch_content)

    for response in responses:
        try:
            verification.append(
                extract_tag_text(response, "result", random=False).strip()
            )
            reasoning.append(
                extract_tag_text(response, "reasoning", random=False).strip()
            )
        except:
            print(response)
            raise ValueError("Failed to extract verification")

    df["verify_facts"] = verification
    df["verify_facts_reasoning"] = reasoning

    df_failed = df[df["verify_facts"] == "INVALID"]
    print(f"Identified {len(df_failed)} invalid claims")
    return df


def verify_corruption(df, book_name):
    """
    Verify whether the claims are valid or not
    """
    p = open("../../prompts/verification.md", "r").read()
    summary = open(f"../../data/output/{book_name}/summary.md", "r").read()
    outline = (
        open(f"../../data/output/{book_name}/outline.md", "r")
        .read()
        .split("\n----------------\n")
    )
    claims = df.corrupted_facts.tolist()
    source = df.source.tolist()

    verification = []
    reasoning = []
    prompts = []
    for i, claim in enumerate(tqdm(claims)):
        if type(source[i]) != str:
            sources = [i for i in range(len(outline))]
        else:
            source_text = source[i]
            if "(" in source_text:
                source_text = source_text.split(" (")[0]
            sources = [int(item) - 1 for item in re.findall(r"(\d+)", source_text)]

        all_source = [
            f"## Chapter {s+1} outline\n"
            + extract_tag_text(outline[s], "events", random=False).strip()
            for s in sources
        ]
        source_text = "\n\n".join(all_source)
        prompts.append(
            p.format(book_summary=summary, claim=claim, chapter_outline=source_text)
        )

    df_response = format_batch_openai(
        prompts,
        "../../data/batch/verify_corruption_in.jsonl",
        "../../data/batch/verify_corruption_out.jsonl",
        metadata={
            "model": "gpt-4o-2024-08-06",
            "max_tokens": 1000,
            "temp": 0.0,
            "top_p": 1.0,
            "system_message": "You are an expert at verifying claims from fictional narratives.",
        },
    )
    responses = df_response.response.apply(extract_batch_content)

    for response in responses:
        verification.append(extract_tag_text(response, "result", random=False).strip())
        reasoning.append(extract_tag_text(response, "reasoning", random=False).strip())

    df["verify_corruption"] = verification
    df["verify_corruption_reasoning"] = reasoning

    df_failed = df[df["verify_corruption"] == "VALID"]
    print(f"Identified {len(df_failed)} invalid claims")
    return df


def duplicate_claims(claim_df):
    """
    Remove duplicate claims
    """
    all_claims = claim_df.facts.tolist()
    claim_list = [f"{i+1}. {claim}" for i, claim in enumerate(all_claims)]
    prompt = (
        open("../../prompts/duplication.md", "r")
        .read()
        .format(fact_list="\n".join(claim_list))
    )
    retry = 0
    while retry < 2:
        try:
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
            )

            # Extracting the answers
            if "<answer>" not in response and not re.search(r"\d", response):
                claim_df["duplication"] = ["Unique" for i in range(len(all_claims))]
                claim_df["duplication_reasoning"] = [
                    "Unique claim" for i in range(len(all_claims))
                ]
                print("No duplicates found")
                return claim_df
            answer = extract_tag_text(response, "answer", random=False).strip()
            answers = [re.sub(r"\- ", "", a) for a in answer.split("\n") if len(a) > 0]
            if len(answers) == 0:
                claim_df["duplication"] = ["Unique" for i in range(len(all_claims))]
                claim_df["duplication_reasoning"] = [
                    "Unique claim" for i in range(len(all_claims))
                ]
                print("No duplicates found")
                return claim_df
            all_dups = []
            for a in answers:
                dup_index = [
                    int(item)
                    for item in a.split(": ")[0].split(", ")
                    if len(item) > 0 and item.isnumeric()
                ]
                all_dups.append(dup_index)

            all_dups_flat = [item for sublist in all_dups for item in sublist]
            first_ind = [item[0] for item in all_dups]
            dups_flat = list(set(all_dups_flat) - set(first_ind))

            # extracting explanations
            explanations = extract_tag_text(response, "answer", random=False).strip()
            explanations = [
                re.sub(r"\- ", "", a) for a in explanations.split("\n") if len(a) > 0
            ]
            all_exp = {}
            for a in explanations:
                exp = a.split(": ")[1]
                claims = [
                    item for item in a.split(": ")[0].split(", ") if len(item) > 0
                ]
                for c in claims:
                    all_exp[c] = exp

            dup_final, dup_exp = [], []
            for i in trange(len(all_claims)):
                if i + 1 in dups_flat:
                    dup_final.append("Duplicate")
                    dup_exp.append(all_exp[str(i + 1)])
                else:
                    dup_final.append("Unique")
                    dup_exp.append("Valid claim")

            claim_df["duplication"] = dup_final
            claim_df["duplication_reasoning"] = dup_exp
            print(f"Identified {len(dups_flat)} duplicate claims")
            break
        except:
            print(response)
            traceback.print_exc()
        retry += 1

    return claim_df


def post_processing_main(book_name, source, action_type):
    """
    Dedup -> Verify -> Filter
    """
    if source == "both":
        source = ["single", "multiple"]
    else:
        source = [source]

    for s in source:
        if action_type == "all":
            df = pd.read_csv(f"../../data/output/{book_name}/claims/claims_{s}_raw.csv")
            df = df.drop_duplicates(subset=["facts", "corrupted_facts"]).reset_index(
                drop=True
            )
            df = duplicate_claims(df)
            df = df[df["duplication"] == "Unique"].reset_index(drop=True)
            df.to_csv(
                f"../../data/output/{book_name}/claims/claims_{s}_cleaned.csv",
                index=False,
            )

            df = verify_claims_iterative(df, book_name)
            df = verify_corruption_iterative(df, book_name)
            df.to_csv(
                f"../../data/output/{book_name}/claims/claims_{s}_unfiltered.csv",
                index=False,
            )
            df = df[
                (df["verify_facts"] == "VALID") & (df["verify_corruption"] == "INVALID")
            ].reset_index(drop=True)
            df.to_csv(
                f"../../data/output/{book_name}/claims/claims_{s}.csv", index=False
            )
        elif action_type == "duplicate":
            df = pd.read_csv(f"../../data/output/{book_name}/claims/claims_{s}_raw.csv")
            df = df.drop_duplicates(subset=["facts", "corrupted_facts"]).reset_index(
                drop=True
            )
            df = duplicate_claims(df)
            df.to_csv(
                f"../../data/output/{book_name}/claims/claims_{s}_cleaned.csv",
                index=False,
            )
        elif action_type == "verify":
            df = pd.read_csv(
                f"../../data/output/{book_name}/claims/claims_{s}_cleaned.csv"
            )
            df = df.drop_duplicates(subset=["facts", "corrupted_facts"]).reset_index(
                drop=True
            )
            df = verify_claims_iterative(df, book_name)
            df = verify_corruption_iterative(df, book_name)
            df.to_csv(
                f"../../data/output/{book_name}/claims/claims_{s}_unfiltered.csv",
                index=False,
            )
            df = df[
                (df["verify_facts"] == "VALID") & (df["verify_corruption"] == "INVALID")
            ].reset_index(drop=True)
            df.to_csv(
                f"../../data/output/{book_name}/claims/claims_{s}.csv", index=False
            )
        print(
            f"Extracted {len(df)} claims for {book_name} and saved to ../../data/output/{book_name}/claims_{s}.csv"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract claims from a story")
    parser.add_argument(
        "--book_name", type=str, help="Name of the book to extract claims from"
    )
    parser.add_argument("--source", help="single or multiple or both", default="both")
    parser.add_argument(
        "--action_type", help="verify or duplicate or corrupt or all", default="all"
    )
    args = parser.parse_args()
    book_name = args.book_name
    source = args.source
    action_type = args.action_type

    post_processing_main(book_name, source, action_type)
