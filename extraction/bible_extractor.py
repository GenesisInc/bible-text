""" bible extractor"""

import os
import re
import json

from bs4 import BeautifulSoup

from config.book_order import SINGLE_CHAPTER_BOOKS, BOOK_ORDER


def normalize_book_name(book_name):
    """Normalize book names to use lowercase and spaces for consistency."""
    return book_name.lower().replace("-", " ")


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
    temp_output_file = os.path.join(output_dir, "multi_translation.json")
    save_to_json(extracted_data, temp_output_file)
    print(f"Extracted data saved to {temp_output_file}")


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


def parse_txt_file(file_path, version, is_single_chapter_book=False):
    """Extract verses and text from a .txt file."""
    verses = {}
    current_chapter = None
    current_verse = None
    combined_text = ""

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for span in soup.select(".text"):
        chapternum = span.find("span", class_="chapternum")
        versenum = span.find("sup", class_="versenum")

        if chapternum:
            current_chapter = chapternum.get_text(strip=True).lstrip("0")
            current_verse = "1"  # Reset verse when chapter changes
            combined_text = ""

        if is_single_chapter_book:
            current_chapter = "1"

        if versenum:
            if combined_text and current_chapter and current_verse:
                verses.setdefault(current_chapter, {}).setdefault(current_verse, {})[
                    version
                ] = combined_text.strip()
            current_verse = versenum.get_text(strip=True).lstrip("0")
            combined_text = ""

        clean_text = clean_verse_text(span.get_text(strip=True), chapternum, versenum)
        combined_text += " " + clean_text

    if current_chapter and current_verse and combined_text:
        verses.setdefault(current_chapter, {}).setdefault(current_verse, {})[
            version
        ] = combined_text.strip()

    return verses


def clean_verse_text(raw_text, chapternum, versenum):
    """Clean raw text by removing chapter numbers, verse numbers, and footnotes."""
    if chapternum:
        raw_text = raw_text[len(chapternum.get_text(strip=True)) :]
    if versenum:
        raw_text = raw_text[len(versenum.get_text(strip=True)) :]
    raw_text = re.sub(r"\[[a-z]\]", "", raw_text)  # Remove footnotes
    return raw_text.strip()
