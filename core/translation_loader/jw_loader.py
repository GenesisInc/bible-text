"""load jw-bibles to a json."""

import json
import os
import re
import unicodedata

from core.utils import file_utils


def generate_bible_json(base_path, output_dir, translation="nwt"):
    """Generate structured JSON representation of Bible text files."""
    bible_data = {translation: {}}
    verse_pattern = r"(\d+)\u00A0"

    def process_chapter_file(chapter_path, chapter_number, book_name):
        """Process a single chapter file and extract verses."""
        bible_data[translation][book_name][int(chapter_number)] = {}
        with open(chapter_path, encoding="utf-8") as file:
            text = file.read()
            verses = re.split(verse_pattern, text)
            for i in range(1, len(verses), 2):
                verse_number = verses[i]
                verse_text = clean_text(verses[i + 1].strip())
                bible_data[translation][book_name][int(chapter_number)][
                    verse_number
                ] = verse_text

    def process_book_folder(book_folder):
        """Process a single book folder and its chapters."""
        book_path = os.path.join(base_path, book_folder)
        if not os.path.isdir(book_path):
            print("returing as there is no path: {book_path}")
            return

        book_name = book_folder.split("-", 1)[1].lower()
        bible_data[translation][book_name] = {}

        for chapter_file in sorted(os.listdir(book_path)):
            # print(f"processing {chapter_file}")
            chapter_path = os.path.join(book_path, chapter_file)
            if os.path.isfile(chapter_path):
                chapter_number = chapter_file.split(".")[0]
                process_chapter_file(chapter_path, chapter_number, book_name)

    # Iterate over each book folder and process
    for book_folder in sorted(os.listdir(base_path)):
        process_book_folder(book_folder)

    # Save the structured data to a JSON file
    file_utils.save_to_json(bible_data, f"{output_dir}/{translation}_bible.json")


# Text cleaning function
def clean_text(text):
    """Clean text by removing non-ASCII characters."""
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


def process_and_generate_bible_json(input_dir, output_dir):  # noqa: C901
    """Process multiple translations and generate combined, individual JSON files."""
    combined_data = {}  # To hold all translations
    verse_pattern = r"(\d+)\u00A0"

    def process_chapter_file(
        chapter_path, chapter_number, book_name, translation, combined_data
    ):
        """Process a single chapter file and extract verses."""
        if translation not in combined_data:
            combined_data[translation] = {}
        if book_name not in combined_data[translation]:
            combined_data[translation][book_name] = {}
        if str(chapter_number) not in combined_data[translation][book_name]:
            combined_data[translation][book_name][str(chapter_number)] = {}

        with open(chapter_path, encoding="utf-8") as file:
            text = file.read()
            verses = re.split(verse_pattern, text)
            for i in range(1, len(verses), 2):
                verse_number = verses[i]
                verse_text = clean_text(verses[i + 1].strip())
                combined_data[translation][book_name][str(chapter_number)][
                    verse_number
                ] = verse_text

    def process_book_folder(book_folder, base_path, translation, combined_data):
        """Process a single book folder and its chapters."""
        book_path = os.path.join(base_path, book_folder)
        if not os.path.isdir(book_path):
            return

        book_name = book_folder.split("-", 1)[1].lower()
        if book_name not in combined_data[translation]:
            combined_data[translation][book_name] = {}

        for chapter_file in sorted(os.listdir(book_path)):
            if chapter_file.endswith(".txt"):
                chapter_path = os.path.join(book_path, chapter_file)
                if os.path.isfile(chapter_path):
                    chapter_number = chapter_file.split(".")[0]
                    process_chapter_file(
                        chapter_path,
                        chapter_number,
                        book_name,
                        translation,
                        combined_data,
                    )

    def process_translation_folder(version_dir, version):
        """Process all books in a translation folder."""
        print(
            f'process_translation_folder() "{version}" translation at "{version_dir}" dir'  # noqa: E501
        )

        if version not in combined_data:
            combined_data[version] = {}

        translation_data = {version: {}}
        for book_folder in sorted(os.listdir(version_dir)):
            book_path = os.path.join(version_dir, book_folder)
            if os.path.isdir(book_path):
                process_book_folder(book_folder, version_dir, version, combined_data)
                # Add to translation-specific data for individual file output
                book_name = book_folder.split("-", 1)[1].lower()
                translation_data[version][book_name] = combined_data[version][book_name]

        # Save individual translation JSON file
        file_utils.save_to_json(translation_data, f"{output_dir}/{version}_bible.json")
        print(f"data successfully written to {output_dir}/{version}_bible.json")

    # Process all translations in input_dir
    for translation in os.listdir(input_dir):
        translation_dir = os.path.join(input_dir, translation)
        if os.path.isdir(translation_dir):
            process_translation_folder(translation_dir, translation)

    print(f"Combined data before saving: {json.dumps(combined_data, indent=2)[:500]}")

    # Debugging: Print the structure of combined_data
    total_verses = count_verses(combined_data)
    print(f"Combined data (length): {len(combined_data)}, total_verses: {total_verses}")

    # Restructure combined_data for multi-translation output
    restructured_data = restructure_combined_data(combined_data)

    # Debugging: Check restructured_data structure
    print(f"Restructured data to save: {json.dumps(restructured_data, indent=2)[:500]}")

    # Save multi-translation JSON file
    if restructured_data:
        sort_and_save(restructured_data, f"{output_dir}/multi_translation.json")
        print(f"Multi-translation data written to {output_dir}/multi_translation.json")
    else:
        print("Restructured data is empty. Nothing to save to multi_translation.json.")


def sort_and_save(data, file_path):
    """Sort and save data to a JSON file."""
    try:
        # Sort data
        if isinstance(data, list):
            data.sort()

        # Write to the file
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    except (TypeError, ValueError) as json_error:  # Issues with JSON serialization
        print(f"Error serializing JSON data: {json_error}")
    except FileNotFoundError as file_error:  # File does not exist
        print(f"File not found: {file_path}, error: {file_error}")
    except PermissionError as permission_error:  # File permission issue
        print(f"Permission denied for {file_path}: {permission_error}")
    except OSError as os_error:  # General file system or I/O errors
        print(f"OS error occurred: {os_error}")
    except BaseException as e:  # pylint: disable=broad-exception-caught
        print(f"An unexpected error occurred: {e}")


def count_verses(data):
    """Count the total number of verses in the nested structure."""
    total_verses = 0
    for _, books in data.items():
        for _, chapters in books.items():
            for _, verses in chapters.items():
                total_verses += len(verses)
    return total_verses


def normalize_chapter_number(chapter):
    """Strip leading zeroes from a chapter number."""
    return str(int(chapter))  # Convert to int and back to str to strip leading zeroes


def restructure_combined_data(data):
    """Transform combined_data to the desired multi-translation structure."""
    restructured_data = {}

    for translation, books in data.items():
        for book_name, chapters in books.items():
            if book_name not in restructured_data:
                restructured_data[book_name] = {}
            for chapter_number, verses in chapters.items():
                # Normalize chapter number
                normalized_chapter_number = normalize_chapter_number(chapter_number)
                if normalized_chapter_number not in restructured_data[book_name]:
                    restructured_data[book_name][normalized_chapter_number] = {}
                for verse_number, verse_text in verses.items():
                    if (
                        verse_number
                        not in restructured_data[book_name][normalized_chapter_number]
                    ):
                        restructured_data[book_name][normalized_chapter_number][
                            verse_number
                        ] = {}
                    restructured_data[book_name][normalized_chapter_number][
                        verse_number
                    ][translation] = verse_text
    return restructured_data
