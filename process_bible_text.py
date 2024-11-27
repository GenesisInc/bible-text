"""process_bible_text.py"""

import argparse
import json
import os
import re

import spacy
from bs4 import BeautifulSoup

# from multiprocessing import Pool


# Load spaCy for entity extraction
nlp = spacy.load("en_core_web_sm", disable=["parser"])

# Predefined book order for sorting
BOOK_ORDER = [
    "genesis",
    "exodus",
    "leviticus",
    "numbers",
    "deuteronomy",
    "joshua",
    "judges",
    "ruth",
    "1 samuel",
    "2 samuel",
    "1 kings",
    "2 kings",
    "1 chronicles",
    "2 chronicles",
    "ezra",
    "nehemiah",
    "esther",
    "job",
    "psalms",
    "proverbs",
    "ecclesiastes",
    "song of solomon",
    "isaiah",
    "jeremiah",
    "lamentations",
    "ezekiel",
    "daniel",
    "hosea",
    "joel",
    "amos",
    "obadiah",
    "jonah",
    "micah",
    "nahum",
    "habakkuk",
    "zephaniah",
    "haggai",
    "zechariah",
    "malachi",
    "matthew",
    "mark",
    "luke",
    "john",
    "acts",
    "romans",
    "1 corinthians",
    "2 corinthians",
    "galatians",
    "ephesians",
    "philippians",
    "colossians",
    "1 thessalonians",
    "2 thessalonians",
    "1 timothy",
    "2 timothy",
    "titus",
    "philemon",
    "hebrews",
    "james",
    "1 peter",
    "2 peter",
    "1 john",
    "2 john",
    "3 john",
    "jude",
    "revelation",
]

SINGLE_CHAPTER_BOOKS = {"3 john", "2 john", "jude", "philemon"}


def parse_txt_file(file_path, version, is_single_chapter_book=False):
    """Extract verses and text from a .txt file."""
    verses = {}
    current_chapter = None
    current_verse = None
    combined_text = ""

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for span in soup.select(".text"):
        # Check for chapter and verse spans
        chapternum = span.find("span", class_="chapternum")
        versenum = span.find("sup", class_="versenum")

        # Update chapter number if a chapter span is found
        if chapternum:
            current_chapter = chapternum.get_text(strip=True).lstrip("0")
            current_verse = "1"  # Reset verse to 1 when a new chapter starts
            combined_text = ""

        if is_single_chapter_book:
            current_chapter = "1"

        # Update verse number if a verse span is found
        if versenum:
            # Save the accumulated text for the previous verse
            if combined_text and current_chapter and current_verse:
                if current_chapter not in verses:
                    verses[current_chapter] = {}
                if current_verse not in verses[current_chapter]:
                    verses[current_chapter][current_verse] = {}
                verses[current_chapter][current_verse][version] = combined_text.strip()
            current_verse = versenum.get_text(strip=True).lstrip("0")
            combined_text = ""  # Reset combined text for the new verse

        # Clean and accumulate text
        raw_text = span.get_text(strip=True)
        clean_text = clean_verse_text(raw_text, chapternum, versenum)
        combined_text += " " + clean_text

    # Save the last accumulated verse
    if current_chapter and current_verse and combined_text:
        if current_chapter not in verses:
            verses[current_chapter] = {}
        if current_verse not in verses[current_chapter]:
            verses[current_chapter][current_verse] = {}
        verses[current_chapter][current_verse][version] = combined_text.strip()

    return verses


def clean_verse_text(raw_text, chapternum, versenum):
    """Clean raw text by removing chapter numbers, verse numbers, and footnotes."""
    # Remove chapter number from the start
    if chapternum:
        raw_text = raw_text[len(chapternum.get_text(strip=True)) :]

    # Remove verse number from the start
    if versenum:
        raw_text = raw_text[len(versenum.get_text(strip=True)) :]

    # Remove footnote markers (e.g., "[a]")
    raw_text = re.sub(r"\[[a-z]\]", "", raw_text)

    # Fix spacing issues
    raw_text = re.sub(r"([a-z])([A-Z])", r"\1 \2", raw_text)
    raw_text = re.sub(r"([a-z])([0-9])", r"\1 \2", raw_text)

    return raw_text.strip()


def extract_verses_from_txt(input_dir, output_dir):
    """Extract verses from .txt files and save as temporary JSON."""
    extracted_data = {}

    for version in os.listdir(input_dir):  # E.g., ASV, KJ21
        version_dir = os.path.join(input_dir, version)
        if not os.path.isdir(version_dir):
            continue

        for book in os.listdir(version_dir):  # E.g., Ruth, Zechariah
            book_dir = os.path.join(version_dir, book)
            if not os.path.isdir(book_dir):
                continue

            # Detect single-chapter books (e.g., "3 John")
            is_single_chapter_book = book.lower() in SINGLE_CHAPTER_BOOKS

            for chapter_file in os.listdir(book_dir):  # E.g., 1.txt, 2.txt
                if chapter_file.endswith(".txt"):
                    file_path = os.path.join(book_dir, chapter_file)

                    print(f"Extracting from {file_path}...")
                    book_name = normalize_book_name(book)
                    if book_name not in extracted_data:
                        extracted_data[book_name] = {}

                    verses = parse_txt_file(
                        file_path, version.lower(), is_single_chapter_book
                    )

                    # Ensure single-chapter books have a chapter "1"
                    if is_single_chapter_book and "1" not in extracted_data[book_name]:
                        extracted_data[book_name]["1"] = {}

                    for chapter, verses_data in verses.items():
                        if chapter not in extracted_data[book_name]:
                            extracted_data[book_name][chapter] = {}
                        for verse, translations in verses_data.items():
                            if verse not in extracted_data[book_name][chapter]:
                                extracted_data[book_name][chapter][verse] = {}
                            extracted_data[book_name][chapter][verse].update(
                                translations
                            )

    # Save extracted data for review
    os.makedirs(output_dir, exist_ok=True)
    temp_output_file = os.path.join(output_dir, "extracted_data2.json")
    save_to_json(extracted_data, temp_output_file)
    print(f"Extracted data saved to {temp_output_file}")


def normalize_book_name(book_name):
    """Normalize book names to use lowercase and spaces for consistency."""
    return book_name.lower().replace("-", " ")


def sort_bible_data(bible_data):
    """Sort Bible data by predefined order."""
    sorted_data = {}
    for book in BOOK_ORDER:
        if book in bible_data:
            chapters = bible_data[book]
            sorted_chapters = {
                str(ch): verses
                for ch, verses in sorted(
                    ((int(c), v) for c, v in chapters.items()), key=lambda x: x[0]
                )
            }
            sorted_data[book] = sorted_chapters
    return sorted_data


def save_to_json(data, output_file):
    """Save hierarchical data to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sort_bible_data(data), f, ensure_ascii=False, indent=4)


def main():
    """main"""
    parser = argparse.ArgumentParser(description="Process Bible text files.")
    parser.add_argument(
        "--input-dir", type=str, required=True, help="Input directory with .txt files."
    )
    parser.add_argument(
        "--output-dir", type=str, required=True, help="Output directory for JSON."
    )
    args = parser.parse_args()
    extract_verses_from_txt(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
