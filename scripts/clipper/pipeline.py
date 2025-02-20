# Run a bunch of scripts in sequence to generate the final output
import sys
sys.path.append("../")
from utils import *
from extraction import extraction_main
from post_processing import post_processing_main
from outline_gen import outline_gen_main
import pandas as pd 
import sys
import traceback
from tqdm import tqdm
import re

def format_data(row): 
    '''
    Format the data into the format for the fine-tuning task
    '''
    prompt = open("../../prompts/eval.md", "r").read()
    book = row['book_name']
    assert len(row['facts'].strip()) > 0, "Empty facts"
    assert len(row['corrupted_facts'].strip()) > 0, "Empty corrupted facts"
    
    if book in os.listdir("../../data/books/"): 
        texts = [open(f"../../data/books/{book}/" + f, 'r').read() for f in os.listdir(f"../../data/books/{book}/") if f.endswith(".txt")]

    book_texts = "\n\n\n\n".join(texts)
    prompt = prompt.replace("{book_text}", book_texts)
    prompt_true = prompt.replace("{claim}", row['facts'])
    try: 
        prompt_false = prompt.replace("{claim}", row['corrupted_facts'])
    except: 
        print(row['corrupted_facts'])
    true_messages = [{"role": "system", "content": "You are an expert at verifying claims from fictional narratives."}, {"role": "user", "content": prompt_true}]
    false_messages = [{"role": "system", "content": "You are an expert at verifying claims from fictional narratives."}, {"role": "user", "content": prompt_false}]

    # Answer
    brainstorm = re.sub(r', item \d+', '', row['brainstorm'])
    true_response = f"<explanation>Here are the relevant details from the text:\n{brainstorm}\n\n{row['fact_reasoning']}</explanation>\n<answer>True</answer>"
    false_response = f"<explanation>Here are the relevant details from the text:\n{brainstorm}\n\n{row['corrupted_reasoning']}</explanation>\n<answer>False</answer>"

    true_messages.append({'role':"assistant", "content": true_response})
    false_messages.append({'role':"assistant", "content": false_response})
    return true_messages, false_messages


def match_case_replacement(match, replacement):
    text = match.group()
    if text.isupper():
        return replacement.upper()
    elif text[0].isupper():
        return replacement.capitalize()
    else:
        return replacement.lower()

def process_text(text):
    try:
        if not isinstance(text, (list, tuple)) or len(text) < 3:
            print(f"Skipping malformed text: {text}")
            return text
        
        content_dict = text[2]
        
        if not isinstance(content_dict, dict) or 'content' not in content_dict:
            return text

        content = content_dict['content']
        if not isinstance(content, str):
            return text
        
        replacements = {
            r"chapter outline": "text",
            r"outline item": "chapter",
            r"outline": "text",
            r"here are the relevant details from the text that support the claim:": "here are the relevant details from the text:"
        }

        for pattern, replacement in replacements.items():
            content = re.sub(
                pattern,
                lambda m: match_case_replacement(m, replacement),
                content,
                flags=re.IGNORECASE
            )

        content_dict['content'] = content
        if isinstance(text[1], dict) and 'content' in text[1]:
            prompt = text[1]['content']
            prompt = prompt.replace(" in at most one paragraph", "").replace("</context>", "</context>\n")
            text[1]['content'] = prompt
        else: 
            print("skipping chat content")
        
        return text 
    
    except Exception as e:
        print(f"An error occurred while processing text: {e}")
        return text


df = pd.read_csv("../../data/books/gutenberg.csv")
book_names = [df.book_name.tolist()[0]]
print("Number of books to be processed:", len(set(book_names)))

claims_df = []
for i, book in tqdm(enumerate(book_names)):
    if str(book) not in os.listdir("../../data/books/"):  
        print(f"Book {book} not found in input directory. Skipping...")
        continue
    os.makedirs(f"../../data/output/{book}/", exist_ok=True)
    os.makedirs(f"../../data/output/{book}/claims", exist_ok=True)
    
    claims_path = f"../../data/output/{book}/claims/"
    outline_gen_main(book)   
    sys.exit()
    if os.path.exists(claims_path):
        if "claims_multiple.csv" in os.listdir(claims_path) and "claims_single.csv" in os.listdir(claims_path):
            print(f"Claims already extracted for {book}. Skipping...")
            continue

    print(f"=== Processing book {book} ({i+1}/{len(book_names)}) ===")
    try: 
        if "outline.md" not in os.listdir(f"../../data/output/{book}"): 
            print("Generating outlines")
            outline_gen_main(book)     
        if "claims_multiple.csv" not in os.listdir(f"../../data/output/{book}/claims/"):
            print("Generating multiple claims")
            if "claim_multiple_raw.csv" not in os.listdir(f"../../data/output/{book}/claims/"):
                extraction_main(book, 10, "multiple")
            post_processing_main(book, "multiple", "all")  
        if "claims_single.csv" not in os.listdir(f"../../data/output/{book}/claims/"):
            print("Generating single claims")
            if "claim_single_raw.csv" not in os.listdir(f"../../data/output/{book}/claims/"):
                extraction_main(book, 10, "single")
            post_processing_main(book, "single", "all")   
    except: 
        traceback.print_exc()
        print(f"Error processing book {book}. Skipping...")
        continue

for i, book in tqdm(enumerate(book_names)):
    # Combine all claims into a single dataframe
    if "claims_multiple.csv" not in os.listdir(f"../../data/output/{book}/claims/"):
        print(f"Multiple claims not found for {book}. Skipping...")
        continue
    claims_multiple = pd.read_csv(f"../../data/output/{book}/claims/claims_multiple.csv")
    claims_multiple['claim_type'] = "multiple"
    if "claims_single.csv" not in os.listdir(f"../../data/output/{book}/claims/"):
        print(f"Single claims not found for {book}. Skipping...")
        continue
    claims_single = pd.read_csv(f"../../data/output/{book}/claims/claims_single.csv")
    claims_single['claim_type'] = "single"
    claims = pd.concat([claims_multiple, claims_single])
    claims['book_name'] = book
    claims_df.append(claims)


all_claims = pd.concat(claims_df).drop_duplicates(subset=["facts"]).reset_index(drop=True)
all_claims['true_messages'], all_claims['false_messages'] = zip(*all_claims.apply(format_data, axis=1))
claims_true = all_claims.rename(columns={"true_messages": "messages"})
claims_true['status'] = "TRUE"
claims_false = all_claims.rename(columns={"false_messages": "messages"})
claims_false['status'] = "FALSE"
claims_final = pd.concat([claims_true, claims_false]).reset_index(drop=True)[['book_name','status','messages','claim_type','facts', 'corrupted_facts']]
claims_final['messages'] = claims_final['messages'].apply(process_text)

claims_final['id'] = range(0, len(claims_final))
claims_final = claims_final.drop_duplicates(subset=['book_name', 'status', 'claim_type', 'facts', 'corrupted_facts']).reset_index(drop=True)

all_claims.to_csv("../../data/output/all_claims.csv", index=False)
single = all_claims[all_claims.claim_type == "single"].reset_index(drop=True)
print("Number of chapter-level claims in the test set: ", len(single))
multiple = all_claims[all_claims.claim_type == "multiple"].reset_index(drop=True)
print("Number of book-level claims in the test set: ", len(multiple))
print("Number of unique books in the test set: ", len(all_claims.book_name.unique()))
