import sys
sys.path.append("../")
from utils import *
import pandas as pd
from tqdm import tqdm
import argparse
import time
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import traceback
torch.cuda.empty_cache()
from vllm import LLM, SamplingParams
import ast
import openai


def vllm_eval(df, claims, corrupted_claims, prompts, model_name='llama', model_dir=None): 
    '''
    Batch inference from vllm
    Given a dataframe of claims, generate inference for each claim
    Replaced the claim only, not the book text
    '''
    if model_name=='prolong': 
        llm = LLM(model=model_dir, max_model_len=512000)        
    elif model_name=='qwen':
        llm = LLM(
            model=model_dir, 
            max_model_len=131072, 
            hf_overrides={"rope_scaling": 
                {"factor": 4.0, "original_max_position_embeddings": 32768, "type": "yarn"}
            }
            )     
    else: 
        llm = LLM(model=model_dir, max_model_len=131072)   
        
    try: 
        tokenizer = llm.get_tokenizer
        print("Tokenizer:", tokenizer.chat_template)
    except:
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        print("Using custom tokenizer")
    sampling_params = SamplingParams(
        temperature=0.0, 
        top_p=1.0, 
        max_tokens=1000, 
        stop_token_ids=[tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")]
    )

    prompt_true, prompt_false = [], []
    for i, claim in enumerate(tqdm(claims)):
        try: 
            true_messages = tokenizer.apply_chat_template([
                {"role": "user", "content": prompts[i].format(claim=claim)},
            ],
            tokenize=False,
            add_generation_prompt=True,)
        except: 
            traceback.print_exc()
        
        try:
            false_messages = tokenizer.apply_chat_template([
                {"role": "user", "content": prompts[i].format(claim=corrupted_claims[i])},
            ],
            tokenize=False,
            add_generation_prompt=True,)
        except:
            traceback.print_exc()
        prompt_true.append(true_messages)
        prompt_false.append(false_messages)

    true_output = llm.generate(prompt_true, sampling_params)
    true_answer, true_reasoning = [], []
    for true_out in tqdm(true_output):
        try:
            assert type(true_out.outputs[0].text) == str
            output_reasoning = true_out.outputs[0].text
            output_answer = extract_tag_text(output_reasoning, "answer", random=False).strip().lower()=='true'
            true_reasoning.append(output_reasoning)
            true_answer.append(output_answer)
            continue
        except:
            print(true_out.outputs[0].text)
            true_reasoning.append("Error")
            true_answer.append("Error")
    df['answer_true'] = true_answer
    df['reasoning_true'] = true_reasoning

    false_answer, false_reasoning = [], []
    false_output = llm.generate(prompt_false, sampling_params)
    for false_out in tqdm(false_output):
        try: 
            assert type(false_out.outputs[0].text) == str
            output_reasoning = false_out.outputs[0].text
            output_answer = extract_tag_text(false_out.outputs[0].text, "answer", random=False).strip().lower()=='false'
            false_reasoning.append(output_reasoning)
            false_answer.append(output_answer)
            continue
        except:
            print(false_out.outputs[0].text)
            false_reasoning.append("Error")
            false_answer.append("Error")

    df['answer_false'] = false_answer
    df['reasoning_false'] = false_reasoning
    return df


def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, help="Models to evaluate", default="claude, gpt-4o, all")
    parser.add_argument("--model_dir", type=str, help="Model directory", default="claude, gpt-4o, all")
    parser.add_argument("--data_input", type=str, help="Input data path", required=True)
    parser.add_argument("--data_output", type=str, help="Output data path", required=True)
    parser.add_argument("--subset", type=str, help="gutenberg or 2024", default="gutenberg")
    parser.add_argument("--start_row", type=int, help="Start row index")
    parser.add_argument("--end_row", type=int, help="End row index")
    parser.add_argument("--chunking", type=str, help="Whether to chunk or not", required=True)
    args = parser.parse_args()

    # Load data (drop duplicates in facts and corrupted facts) ---
    data_input = f"../../data/benchmark/{args.data_input}.csv"
    data_output = args.data_output
    claims_df_batch = pd.read_csv(data_input).drop_duplicates(subset=['facts', 'corrupted_facts']).reset_index(drop=True)
    print("Size of entire dataset:", len(claims_df_batch))
    if args.chunking.lower()=="true": 
        claims_df_batch = claims_df_batch.iloc[args.start_row:args.end_row]
        print(f"Processing {data_input} from row {args.start_row} to {args.end_row}")
    else: 
        print(f"Processing {data_input} from row 0 to {len(claims_df_batch)}")

    # Handle existing output
    if os.path.exists(data_output):
        existing_df = pd.read_csv(data_output)
        print(f"Loaded existing output from {data_output}")

        # Check if claims in existing data match the input data 
        existing_facts = existing_df['facts'].tolist()
        input_facts = claims_df_batch.iloc[:len(existing_facts)]['facts'].tolist()
        if existing_facts != input_facts:
            print("Mismatch between existing facts and input data. Running the full data.")
        else: 
            if len(existing_df) >= len(claims_df_batch):
                print("All data has been processed. Exiting.")
                return
            print("Existing data matches the input data. Resuming processing.")
            claims_df_batch = claims_df_batch.iloc[len(existing_df):]
    
    # Subset data based on the number of tokens that a model can handle
    if args.subset == "nocha" and args.model in ["llama", "qwen"]: 
        claims_df_batch = claims_df_batch[claims_df_batch.length<=128000].reset_index(drop=True)

    # Generate prompts based on book text inclusion
    prompts = []
    if args.subset == "wp": 
        col = "id"
    else: 
        col = "book_name" if "book_name" in claims_df_batch.columns else "book_title"
    for i, book in enumerate(claims_df_batch[col].tolist()):
        book = str(book)
        if args.subset == "gutenberg":
            if book in os.listdir(f"../../data/books/"): 
                all_chaps = sorted(os.listdir(f"../../data/books/{book}/"), key=lambda x: int(x.split(".")[0]))
                texts = [open(f"../../data/books/{book}/" + f, 'r').read() for f in all_chaps]
            else: 
                print(f'Cannot find {book}. Exiting...')
                sys.exit()
            book_texts = "\n\n\n\n".join(texts)
        else: 
            book_texts = open(f"../../data/input/{book}/full.txt", 'r').read()
        

        eval_prompt = open("../../prompts/eval.md", 'r').read()
        book_texts = book_texts.replace("{", "").replace("}", "")
        prompts.append(eval_prompt.replace("{book_text}", book_texts))

    facts = claims_df_batch.facts.tolist()
    corrupted_facts = claims_df_batch.corrupted_facts.tolist()

    #df = vllm_eval(claims_df_batch, facts, corrupted_facts, prompts, args.model.lower(), args.model_dir)
    print("prompting", args.model_dir)
    df = vllm_eval(claims_df_batch, facts, corrupted_facts, prompts, args.model.lower(), args.model_dir)
    # Save output ---
    if args.model.lower() not in ['gpt-4o', 'o1-mini']: 
        if os.path.exists(data_output):
            df.to_csv(data_output, mode='a', header=False, index=False)
        else:
            df.to_csv(data_output, index=False)

        print("Overall accuracy:", len(df[(df.answer_true==True) & (df.answer_false==True)].reset_index(drop=True)) / len(df) * 100)
        print("Number of errors:", len(df[(df.answer_true == "Error") | (df.answer_false == "Error")].reset_index(drop=True)))

if __name__ == "__main__":
    main()