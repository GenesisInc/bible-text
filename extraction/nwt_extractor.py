""" extract nwt"""

import os
import json
import re
import unicodedata


def generate_bible_json(base_path, output_file):
    """Generates a structured JSON representation of Bible text files."""
    bible_data = {"nwt": {}}
    verse_pattern = r"(\d+)\u00A0"

    for book_folder in sorted(os.listdir(base_path)):
        book_path = os.path.join(base_path, book_folder)
        if os.path.isdir(book_path):
            book_name = book_folder.split("-", 1)[1].lower()
            bible_data["nwt"][book_name] = {}
            for chapter_file in sorted(os.listdir(book_path)):
                chapter_path = os.path.join(book_path, chapter_file)
                if os.path.isfile(chapter_path) and chapter_file.isdigit():
                    chapter_number = int(chapter_file)
                    bible_data["nwt"][book_name][str(chapter_number)] = {}
                    with open(chapter_path, "r", encoding="utf-8") as file:
                        text = file.read()
                        verses = re.split(verse_pattern, text)
                        for i in range(1, len(verses), 2):
                            verse_number = verses[i]
                            verse_text = clean_text(verses[i + 1].strip())
                            bible_data["nwt"][book_name][str(chapter_number)][
                                verse_number
                            ] = verse_text

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(bible_data, json_file, indent=4)
    print(f"Bible data successfully written to {output_file}")


# Text cleaning function
def clean_text(text):
    """Cleans text by removing non-ASCII characters, normalizing unicode,
    and adding spaces where needed."""
    text = text.replace("\u2014", " ")  # Replace em dash with space
    text = "".join(
        c
        for c in unicodedata.normalize("NFKD", text)
        if ord(c) < 128  # Keeps ASCII only
    )
    text = text.replace("\n", " ").replace("-", " ")
    text = re.sub(r"(?<!\d)([,;:])(?!\d)([^\s])", r"\1 \2", text)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    return text
