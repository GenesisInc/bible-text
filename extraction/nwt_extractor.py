""" extract nwt"""

import os
import re
import unicodedata

from utils import file_utils


def generate_bible_json(base_path, output_file):
    """Generates a structured JSON representation of Bible text files."""
    bible_data = {"nwt": {}}
    verse_pattern = r"(\d+)\u00A0"

    def process_chapter_file(chapter_path, chapter_number, book_name):
        """Process a single chapter file and extract verses."""
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

    def process_book_folder(book_folder):
        """Process a single book folder and its chapters."""
        book_path = os.path.join(base_path, book_folder)
        if not os.path.isdir(book_path):
            return

        book_name = book_folder.split("-", 1)[1].lower()
        bible_data["nwt"][book_name] = {}

        for chapter_file in sorted(os.listdir(book_path)):
            if chapter_file.isdigit():  # Ensure chapter file is numeric
                chapter_path = os.path.join(book_path, chapter_file)
                if os.path.isfile(chapter_path):
                    chapter_number = int(chapter_file)
                    process_chapter_file(chapter_path, chapter_number, book_name)

    # Iterate over each book folder and process
    for book_folder in sorted(os.listdir(base_path)):
        process_book_folder(book_folder)

    # Save the structured data to a JSON file
    file_utils.save_to_json(bible_data, output_file)


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
