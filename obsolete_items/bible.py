"""process bible text"""

import argparse
import csv
import json
import os
import re
import sys
import unicodedata

# from multiprocessing import Pool

import spacy

# Load spaCy's English model with only the NER component
nlp = spacy.load("en_core_web_sm", disable=["parser"])

# Occupation keywords for matching
occupation_keywords = {
    "apothecary",
    "architect",
    "armor maker",
    "armor-bearer",
    "astrologer",
    "astronomer",
    "baker",
    "beggar",
    "blacksmith",
    "builder of city walls",
    "camel driver",
    "caretaker of sacred items",
    "carpenter",
    "charioteer",
    "chief of army",
    "choir member",
    "cook",
    "cupbearer",
    "cupmaker",
    "dancer",
    "dealer in purple cloth",
    "dyer",
    "elder",
    "executioner",
    "farmer",
    "fisher",
    "fisherman",
    "flock herder",
    "gatekeeper",
    "goldsmith",
    "governor",
    "harvester",
    "herder",
    "high priest",
    "horseman",
    "hunter",
    "judge",
    "king",
    "lawyer",
    "linen worker",
    "mason",
    "merchant",
    "metalworker",
    "midwife",
    "miller",
    "musician",
    "perfumer",
    "physician",
    "potter",
    "priest’s assistant",
    "priest",
    "prophet",
    "queen",
    "sandal maker",
    "scout",
    "scribe",
    "servant",
    "shepherd",
    "shipbuilder",
    "shipmaster",
    "singer",
    "slave",
    "slavegirl",
    "soldier",
    "spy",
    "stonecutter",
    "tax collector",
    "teacher",
    "temple servant",
    "tent weaver",
    "tent-dweller",
    "tentmaker",
    "trader",
    "vineyard keeper",
    "weaver",
    "winemaker",
}


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


def load_to_json(base_path, output_file):
    """Generates a structured JSON representation of Bible text files."""
    bible_data = {"nwt": {}}
    verse_pattern = r"(\d+)\u00A0"

    for book_folder in sorted(os.listdir(base_path)):
        book_path = os.path.join(base_path, book_folder)
        if os.path.isdir(book_path):
            print(f"book_path = {book_path}")
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


def main():
    """Main function to handle CLI."""
    parser = argparse.ArgumentParser(
        description="Process Bible text and extract entities."
    )
    parser.add_argument(
        "--load-to-json",
        action="store_true",
        help="Generate Bible JSON from text files",
    )
    parser.add_argument(
        "--base-path",
        type=str,
        help="Base path of Bible text files",
        default="data/bibles",
        # default="../newWorldTranslation/english/2013-release",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        help="Output JSON file path",
        default="data/bible_entities.json",
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        help="Output CSV file path",
        default="data/bible_entities.csv",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Output the results in CSV format",
    )

    args = parser.parse_args()

    if args.load_to_json:
        load_to_json(args.base_path, args.bible_json)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
