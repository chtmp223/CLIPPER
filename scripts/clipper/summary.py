import sys
sys.path.append("../")
from utils import * 
import argparse
import pandas as pd
from tqdm import tqdm
import os


def get_summary(book_name): 
    '''
    Generating summary for one book
    '''
    book_text = open(f"../../data/books/{book_name}.txt", "r").read()
    if count_tiktoken(open(f"../../prompts/summary.md", "r").read().format(book=book_text), "gpt-4o") > 124000:
        book_text = truncating_tokens(book_text, 124000)
    summary_prompt = open(f"../../prompts/summary.md", "r").read().format(book=book_text)

    print("Generating summary for", book_name)
    summary = prompt_openai(summary_prompt, True, {"model": "gpt-4o-2024-08-06", "temp": 0.5, "top_p": 1.0,"max_tokens": 2000})

    return summary


def batch_summary(): 
    '''
    Batch generate summaries for all books
    '''
    book_df = pd.read_csv("../../data/metadata/gutenberg.csv")
    books = book_df.book_name.tolist()
    if "summary" in book_df.columns and type(book_df["summary"].tolist()[0]) == str:
        book_existing = book_df[(book_df["summary"].str.len() > 0)| (book_df['num_tokens'] > 128000)]
    else: 
        book_existing = pd.DataFrame(columns=book_df.columns)

    summary_prompt = open(f"../../prompts/summary.md", "r").read()
    summary_prompts, book_texts, book_names = [], [], []
    for book in tqdm(books, description="Preparing books for summary generation"): 
        if book in book_existing.book_name.tolist():  
            continue
        book_chapter = [f"## Chapter {i+1}\n" + open(f"../../data/books/{book}/{f}", 'r').read() for i, f in enumerate(os.listdir(f"../../data/books/{book}"))]
        book_text = "\n\n".join(book_chapter)
        if count_tiktoken(summary_prompt.format(book=book_text), "gpt-4o") > 124000:
            print("Truncating book text for", book)
            book_text = truncating_tokens(book_text, 124000)
        book_texts.append(book_text)
        book_names.append(book)
        summary_prompts.append(summary_prompt.format(book=book_text))

    print("Generating summaries for", len(book_texts), "books")
    os.makedirs("../../data/batch", exist_ok=True)
    book_summary = format_batch_openai(summary_prompts, "../../data/batch/summary_input.jsonl", "../../data/batch/summary_output.jsonl", metadata={"model": "gpt-4o-2024-08-06", "max_tokens": 2000, "temp": 0.5, "top_p": 1.0, "system_message": "You are an expert at summarizing books."})
    summaries = book_summary.response.apply(extract_batch_content)

    for i, book in enumerate(book_names):
        book_df.loc[book_df["book_name"] == book, "summary"] = summaries[i]
    print(len(book_df[book_df["summary"].str.len() == 0]), "books failed to generate summary")
    return book_df


def main(): 
    parser = argparse.ArgumentParser(description='Summarize a book')
    parser.add_argument('--book_name', type=str, help='Name of the book to summarize (if not using batch)', required=False)
    parser.add_argument('--batch', type=str, help='Batch generate summaries for all books (batch or nope)', default='batch')
    args = parser.parse_args()

    if args.book_name is None:
        df = pd.read_csv("../../data/books/metadata/gutenberg.csv")
        books = df.book_name.tolist()
    else: 
        books = [args.book_name]

    if args.batch.lower().strip() == "nope":
        for book_name in tqdm(books): 
            if args.summary_type == "summary": 
                summary = get_summary(book_name)
                with open(f"../../data/output/{book_name}/summary.md", "w") as f: 
                    f.write(summary)
    else:   #batch summary
        df = batch_summary()
        df.to_csv("../../data/books/metadata/gutenberg.csv", index=False)

        for i, row in df.iterrows(): 
            if not os.path.exists(f"../../data/output/{row['book_name']}"):
                os.makedirs(f"../../data/output/{row['book_name']}", exist_ok=True)
            with open(f"../../data/output/{row['book_name']}/summary.md", "w") as f: 
                try: 
                    if row["summary"] is None:
                        row["summary"] = ""
                    f.write(row["summary"])
                except: 
                    print("Error writing summary for", row['book_name'])
                    print(row["summary"])


if __name__ == "__main__":
    main()
