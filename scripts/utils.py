import os
from openai import OpenAI
import re
import tiktoken
import vertexai
import json
import time
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    SafetySetting,
    Part,
)
from transformers import pipeline
from datasets import Dataset, DatasetDict
from vllm import LLM, SamplingParams
import vertexai
from anthropic import AnthropicVertex
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from tqdm import trange
from sklearn import metrics
import numpy as np
import pandas as pd

# ---* Prompting API *----
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"], organization=os.environ["OPENAI_API_ORG"]
)


def prompt_openai(
    prompt,
    verbose=False,
    metadata={
        "model": "gpt-4o-2024-08-06",
        "temp": 1.0,
        "top_p": 1.0,
        "max_tokens": 4095,
    },
    system_message="You are a helpful assistant.",
):
    """
    Given a prompt and metadata, return the completion from OpenAI's API.
    """
    completion = client.chat.completions.create(
        model=metadata["model"],
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
        max_tokens=metadata["max_tokens"],
        temperature=metadata["temp"],
        top_p=metadata["top_p"],
    )
    if verbose:
        print("Prompt usage:", completion.usage.prompt_tokens)
        print("Response usage:", completion.usage.completion_tokens)

    return completion.choices[0].message.content


def prompt_claude(
    prompt,
    verbose=True,
    metadata={"model": "claude-3-5-sonnet@20240620", "temp": 1.0, "max_tokens": 4095},
    system_message="You are a helpful assistant.",
    project_id=os.environ["VERTEX_PROJECT_ID"],
):
    """
    Prompt Claude with VertexAI API
    - prompt: The prompt to be sent to the model
    - verbose: Print usage details
    - metadata: Model metadata (model, temp, max_tokens)
    - system_message: System message
    - project_id: Google Cloud project ID
    """
    client = AnthropicVertex(region="europe-west1", project_id=project_id)
    message = client.messages.create(
        model=metadata["model"],
        max_tokens=metadata["max_tokens"],
        temperature=metadata["temp"],
        system=system_message,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    message_json_str = message.model_dump_json(indent=2)
    message_dict = json.loads(message_json_str)
    text_content = message_dict["content"][0]["text"]
    if verbose:
        print(
            "Prompt usage:",
            message_dict["usage"]["input_tokens"],
            f"${message_dict['usage']['input_tokens']/1000000*3}",
        )
        print(
            "Prompt usage:",
            message_dict["usage"]["output_tokens"],
            f"${message_dict['usage']['output_tokens']/1000000*15}",
        )
    return text_content.strip()


def format_batch_openai(
    prompts,
    input_fpath,
    output_fpath,
    metadata={
        "model": "gpt-4o-2024-08-06",
        "max_tokens": 4095,
        "temp": 0.0,
        "top_p": 1.0,
        "system_message": "You are a helpful assistant.",
    },
):
    """
    Create new batch request based on the prompts (OpenAI batch API)
    """
    entries = []
    for i, prompt in enumerate(prompts):
        message = [
            {"role": "system", "content": metadata["system_message"]},
            {"role": "user", "content": prompt},
        ]
        entry = {
            "custom_id": f"request-{i}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": metadata["model"],
                "max_tokens": metadata["max_tokens"],
                "top_p": metadata["top_p"],
                "temperature": metadata["temp"],
                "messages": message,
            },
        }
        entries.append(entry)

    with open(input_fpath, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

    batch_input_file = client.files.create(
        file=open(input_fpath, "rb"), purpose="batch"
    )
    batch_input_file_id = batch_input_file.id

    batch = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": "Chau's batch"},
    )

    # Retrieve and extract batch content
    while not client.batches.retrieve(batch.id).output_file_id:
        print("Waiting an additional of 20 seconds for the batch to complete")
        time.sleep(20)
    out_id = client.batches.retrieve(batch.id).output_file_id
    file_response = client.files.content(out_id)

    # Write the output to a file
    with open(output_fpath, "w") as f:
        f.write(file_response.text)

    df = pd.read_json(output_fpath, lines=True)
    return df


def count_tiktoken(messages, model):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using o200k_base encoding.")
        encoding = tiktoken.get_encoding("o200k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        "gpt-4o-2024-08-06",
        "claude",
        "claude-3-5-sonnet@20240620",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print(
            "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return count_tiktoken(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4o."
        )
        return count_tiktoken(messages, model="gpt-4o-2024-08-06")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}."""
        )
    num_tokens = tokens_per_message + len(encoding.encode(messages))
    num_tokens += 3
    return num_tokens


def truncating_tokens(document, max_tokens, model="gpt-4o"):
    """
    Truncating the document down to contain only a max_tokens number of tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using o200k_base encoding.")
        encoding = tiktoken.get_encoding("o200k_base")
    tokens = encoding.encode(document)
    if len(tokens) + 3 > max_tokens:
        tokens = tokens[: max_tokens - 3]
    return encoding.decode(tokens)


def extract_batch_content(obj):
    text = obj["body"]["choices"][0]["message"]["content"]
    return text


# ---* Random utils *---
def extract_tag_text(text, tag, random=False):
    """
    Extract text between two tags
    random=True: Extracts text between the first tag and the next tag
    random=False: Extracts text between the first tag and the closing tag
    """
    if random:
        pattern = re.compile(rf"<{tag}>(.*?)<(.*?)>", re.DOTALL)
    else:
        pattern = re.compile(rf"<{tag}>(.*?)</{tag}>", re.DOTALL)

    return pattern.findall(text)[0]


def insert_closing_tag(text):
    """
    Insert missing closing tags to the text
    """
    tags = re.findall(r"<(\w*?)>", text)
    missing_tags = [tag for tag in tags if f"</{tag}>" not in text]

    for tag in missing_tags:
        in_text = extract_tag_text(text, tag, random=True)[0]
        text = text.replace(in_text, f"{in_text.strip()}</{tag}>\n\n")

    return text


def clean_word(text):
    # Deal with situation where the word ends with 're, 's, 't, etc.
    # However, we don't want to remove O'Connor, O'Neil, etc.
    to_remove = ["'re", "'s", "'t", "'ve", "'ll", "'d", "'m"]
    for r in to_remove:
        if text.endswith(r):
            find_index = text.find(r)
            text = text[:find_index]
    return re.sub(r"[^a-zA-Z]", "", text)
