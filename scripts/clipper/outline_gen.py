import argparse
import os
import sys

sys.path.append("../")
from utils import *
from tqdm import trange
import traceback
import re

FILLER = ["mr", "mrs", "dr", "new", "existing", "and", "or", "/"]


def get_chapters(book_name):
    """
    Given a book name, return a list of chapters in the book.
    """
    book_name = str(book_name)
    chapters = []
    if book_name in os.listdir(f"../../data/books/"):
        folder = [
            f
            for f in os.listdir(f"../../data/books/{book_name}")
            if f.endswith(".txt") and f != "full.txt"
        ]
        folder = sorted(folder, key=lambda x: int(x.split(".")[0]))
        for f in folder:
            chapter = open(f"../../data/books/{book_name}/{f}", "r").read()
            chapters.append(chapter)
        return chapters
    else:
        raise Exception("Book not found")


def outline_gen(book_name, chapters):
    """
    Given the previously generated chapter outlines and the order of the current chapter, generate the outline for the book.
    """
    story_prompt = open("../../prompts/outline.md", "r").read()
    previous_chapters = []

    # Go through each chapter and generate the outline
    for i in trange(len(chapters)):
        prompt = story_prompt.replace("{order}", str(i + 1))
        prompt = prompt.replace("{curr}", chapters[i])
        prompt = re.sub(r"\n{3,}", "\n", prompt)

        retry = 0
        while retry < 3:  # Retry if the formatting is not correct
            try:
                if retry > 0:
                    time.sleep(100)
                    prompt += "You need to generate a chapter outline that follows the specified format!"
                outline = prompt_claude(
                    prompt,
                    verbose=False,
                    metadata={
                        "model": "claude-3-5-sonnet@20240620",
                        "temp": 0.0,
                        "max_tokens": 4096,
                        "top_p": 1.0,
                    },
                    system_message="You are an expert at creating objective outlines of fictional narratives.",
                )
                if (
                    "<synopsis>" in outline
                    and "<events>" in outline
                    and "<characters>" in outline
                ):
                    outline = "<synopsis>" + outline.split("<synopsis>")[1]
                    outline = outline.split("</characters>")[0] + "</characters>"
                    previous_chapters.append(outline)
                    break
                else:
                    print(
                        f"Wrong outline format for chapter {i}. Retrying #{retry+1}..."
                    )
            except Exception as e:
                traceback.print_exc()
            retry += 1

        if not (
            "<synopsis>" in outline
            and "<events>" in outline
            and "<characters>" in outline
        ):
            print("Failed to generate outline for chapter", i)
            os.remove(f"../../data/output/{book_name}/outline.md")
            return
        with open(f"../../data/output/{book_name}/outline.md", "a+") as f:
            f.write("# Chapter " + str(i + 1) + "\n" + outline + "\n----------------\n")
    return previous_chapters


def post_processing(outlines):
    """
    Clean up character list such that no character that is not already mentioned in the
    events list is added to the character list.
    Add closing tags
    """
    new_out = []
    for i, out in enumerate(outlines):
        try:
            if (
                "</events>" not in out
                or "</characters>" not in out
                or "</synopsis>" not in out
            ):
                out = insert_closing_tag(out)
            synopsis = extract_tag_text(out, "synopsis")
            events = extract_tag_text(out, "events")
            previous_text = synopsis + events

            previous_text = [
                clean_word(word.lower()) for word in previous_text.split(" ")
            ]
            characters = extract_tag_text(out, "characters")
            characters = characters.split("\n")

            final_characters = []
            for char in characters:
                name = ". ".join(char.split(":")[0].split(". ")[1:])
                if " " in name:
                    names = name.split(" ")
                    adding = False
                    for n in names:
                        n = clean_word(n.lower())
                        if n in previous_text and n not in FILLER:
                            adding = True
                    if len(name) > 0 and adding == True:
                        char = (
                            name.strip("[]")
                            + ": "
                            + ":".join(char.split(":")[1:]).strip()
                        )
                        final_characters.append(char)
                else:
                    to_check = clean_word(name.lower())
                    if to_check in previous_text and len(to_check) > 0:
                        char = name.strip("[]") + ":" + ":".join(char.split(":")[1:])
                        final_characters.append(char)

            new_characters = "\n".join(
                [f"{i+1}. {char}" for i, char in enumerate(final_characters)]
            )
            out = out.replace(extract_tag_text(out, "characters"), new_characters)
            new_out.append(out)
        except:
            print("Error in post processing:", i)
            traceback.print_exc()
            new_out.append("ERROR")
    return new_out


def gen_character_status(outlines):
    """
    Return the character list for each chapter & format the character list to show existing and new characters.
    Does not cover cases where multiple characters have the same last name.
    - outlines: list of outlines for each chapter
    """
    characters = set()
    character_dict = dict()
    affliations = []
    out = []
    for i, outline in enumerate(outlines):
        character_status = {"existing": [], "new": []}
        character = [
            line
            for line in extract_tag_text(outline, "characters").split("\n")
            if len(line) > 0
        ]
        chars = [
            ". ".join(char.strip().split(":")[0].split(". ")[1:]) for char in character
        ]
        splitted = [
            clean_word(n.lower())
            for name in chars
            for n in name.split(" ")
            if clean_word(n.lower()) not in FILLER and len(clean_word(n.lower())) > 0
        ]
        affliation = []
        for j, name in enumerate(chars):
            if " " in name:
                names = name.split(" ")
                adding = False
                for n in names:
                    n = clean_word(n.lower())
                    if n in characters and n not in FILLER:
                        adding = True
                if len(name) > 0 and adding == True:
                    char = (
                        character[j].split(": ")[0]
                        + " (existing): "
                        + ": ".join(character[j].split(": ")[1:])
                    )
                    affliation.append(char)
                    character_status["existing"].append(name)
                else:
                    char = (
                        character[j].split(": ")[0]
                        + " (new): "
                        + ": ".join(character[j].split(": ")[1:])
                    )
                    affliation.append(char)
                    character_status["new"].append(name)
            else:
                to_check = clean_word(name.lower())
                if to_check in characters and len(to_check) > 0:
                    char = (
                        character[j].split(": ")[0]
                        + " (existing): "
                        + ": ".join(character[j].split(": ")[1:])
                    )
                    affliation.append(char)
                    character_status["existing"].append(name)
                else:
                    char = (
                        character[j].split(": ")[0]
                        + " (new): "
                        + ": ".join(character[j].split(": ")[1:])
                    )
                    affliation.append(char)
                    character_status["new"].append(name)
        character_dict["chapter_" + str(i + 1)] = character_status
        affliations.append("\n".join(affliation))
        characters.update(splitted)

        out.append(
            outlines[i].replace(
                extract_tag_text(outlines[i], "characters"),
                "</characters>" + "\n".join(affliation) + "</characters>",
            )
        ).replace("<characters><characters>", "<characters>").replace(
            "</characters></characters>", "</characters>"
        )
    return character_dict, out


def outline_gen_main(book_name):
    chapters = get_chapters(book_name)
    os.makedirs(f"../../data/output/{book_name}", exist_ok=True)
    if os.path.exists(f"../../data/output/{book_name}/outline.md"):
        os.remove(f"../../data/output/{book_name}/outline.md")
    outlines = outline_gen(book_name, chapters)
    assert len(outlines) == len(
        chapters
    ), "Number of outlines generated does not match the number of chapters"

    outlines = (
        open(f"../../data/output/{book_name}/outline.md", "r")
        .read()
        .split("----------------")
    )
    outlines = [item.strip() for item in outlines if item.strip() != ""]
    outlines = post_processing(outlines)
    with open(f"../../data/output/{book_name}/outline.md", "w") as f:
        f.write("\n----------------\n".join(outlines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an outline for a book")
    parser.add_argument(
        "--book_name", type=str, help="The name of the book to generate an outline for"
    )
    args = parser.parse_args()
    book_name = args.book_name
    outline_gen_main(book_name)
