"""load gateway-bibles to a json."""

import os
import re

from bs4 import BeautifulSoup

from config.book_order import SINGLE_CHAPTER_BOOKS
from core.utils import file_utils
from core.utils.logger_utils import get_logger

logger = get_logger(__file__.rsplit("/", 1)[-1])


def normalize_book_name(book_name):
    """Normalize book names to use lowercase and spaces for consistency."""
    return book_name.lower().replace("-", " ")


def extract_verses_from_txt(input_dir, output_dir):  # noqa: C901
    """Extract verses from .txt files and save as multi-translation.json."""
    extracted_data = {}

    def process_chapter(file_path, version, book_name, is_single_chapter_book):
        """Process a single chapter file and update the extracted data."""
        verses = parse_txt_file(
            book_name, file_path, version.lower(), is_single_chapter_book
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
                extracted_data[book_name][chapter][verse].update(translations)

    def process_book(version_dir, version):
        """Process all chapters in a book directory."""
        for book in os.listdir(version_dir):  # E.g., Ruth, Zechariah
            book_dir = os.path.join(version_dir, book)
            if not os.path.isdir(book_dir):
                continue

            is_single_chapter_book = book.lower() in SINGLE_CHAPTER_BOOKS
            book_name = normalize_book_name(book)
            if book_name not in extracted_data:
                extracted_data[book_name] = {}

            for chapter_file in os.listdir(book_dir):  # E.g., 1.txt, 2.txt
                if chapter_file.endswith(".txt"):
                    file_path = os.path.join(book_dir, chapter_file)
                    # print(f"Extracting from {file_path}...")
                    process_chapter(
                        file_path, version, book_name, is_single_chapter_book
                    )

    # Process each version in the input directory
    for version in os.listdir(input_dir):  # E.g., ASV, KJ21
        version_dir = os.path.join(input_dir, version)
        if not os.path.isdir(version_dir):
            continue
        process_book(version_dir, version)

    # Save extracted data for review
    file_utils.sort_and_save(extracted_data, f"{output_dir}/multi_translation.json")


def parse_txt_file(book_name, file_path, version, is_single_chapter_book=False):
    """Extract verses and text from a .txt file."""
    verses = {}
    current_chapter = None
    current_verse = None
    combined_text = ""

    with open(file_path, encoding="utf-8") as f:
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

        clean_text = clean_verse_text(
            span.get_text(strip=True),
            f"{version}.{book_name} {current_chapter}:{current_verse}",
            chapternum,
            versenum,
        )
        combined_text += " " + clean_text

    if current_chapter and current_verse and combined_text:
        verses.setdefault(current_chapter, {}).setdefault(current_verse, {})[
            version
        ] = combined_text.strip()

    return verses


def clean_verse_text(raw_text, ref, chapternum, versenum):
    """Clean raw text by removing chapter numbers, verse numbers, and footnotes."""
    if chapternum:
        raw_text = raw_text[len(chapternum.get_text(strip=True)) :]
    if versenum:
        raw_text = raw_text[len(versenum.get_text(strip=True)) :]
    raw_text = re.sub(r"\[[a-z]\]", "", raw_text)  # Remove footnotes
    return fix_unicode_strings(raw_text.strip(), ref)


# Function to fix Unicode and other replacements
def fix_unicode_strings(data, ref):
    """Fix fix_unicode_strings."""
    data_old = data
    if isinstance(data, str):
        # Replace specific Unicode characters
        data = (
            data.replace("\u201c", "“")
            .replace("\u201d", "”")
            .replace("\u2014", "—")
            .replace("\u2018", "‘")
            .replace("\u2019", "’")
            .replace("\u2016", "‖")
            .replace("\u2032", "'")
            .replace("\u00bd", "½")
            .replace("\u00bc", "¼")
            .replace("\u00a0", " ")  # Replace non-breaking space
        )
        # Replace Hebrew characters (e.g., \u05d1 Beth → Beth)
        data = re.sub(r"\\u05d0", "Aleph", data)  # Replace specific Hebrew
        data = re.sub(r"\\u05d1", "Beth", data)
        data = re.sub(r"\\u05d2", "Gimel", data)
        data = re.sub(r"\\u05d3", "Daleth", data)
        data = re.sub(r"\\u05d4", "He", data)
        data = re.sub(r"\\u05d5", "Vav", data)

        if data_old != data:
            logger.debug(f"{ref} \n{data_old} \n{data}")
        return data
    elif isinstance(data, list):
        return [fix_unicode_strings(item) for item in data]
    elif isinstance(data, dict):
        return {key: fix_unicode_strings(value) for key, value in data.items()}
    return data
