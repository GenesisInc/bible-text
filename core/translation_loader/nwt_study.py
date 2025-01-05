# bible-text/core/translation_loader/nwt_study.py
import json
import os

from config.book_order import BOOK_ORDER


def parse_book_to_json(filename, chapter_sep=" ", verse_sep=" "):
    """Parse Bible text into a structured JSON format.

    Args:
        filename (str): Path to the text file containing the Bible book.
        chapter_sep (str): Character(s) indicating the start of a chapter.
        verse_sep (str): Character(s) indicating the start of a verse.

    Returns:
        dict: JSON structure of the parsed Bible text.
    """
    result = {"1": {}}  # Default to chapter "1"
    current_chapter = "1"
    current_verse = None

    with open(filename, encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Detect chapters
            if chapter_sep in line:
                chapter_split = line.split(chapter_sep, 1)
                if chapter_split[0].isdigit():
                    current_chapter = chapter_split[0].strip()
                    result.setdefault(current_chapter, {})
                    current_verse = None  # Reset current verse
                    line = chapter_split[1].strip() if len(chapter_split) > 1 else ""

            # Detect verses
            if verse_sep in line:
                verse_split = line.split(verse_sep, 1)
                if verse_split[0].isdigit():
                    current_verse = verse_split[0].strip()
                    verse_text = verse_split[1].strip() if len(verse_split) > 1 else ""
                    result[current_chapter][current_verse] = verse_text
                    continue

            # Handle first verse if not explicitly marked
            if current_verse is None and current_chapter:
                current_verse = "1"
                result[current_chapter][current_verse] = line.strip()
                continue

            # Append multi-line text to the last detected verse
            if current_chapter and current_verse:
                result[current_chapter][current_verse] += f" {line}"

    return result


def validate_json_files(base_path, translation):
    """Validate JSON files in the specified directory.

    Perform quick checks like line counts and structure validation.

    Args:
        base_path (str): Path to the directory containing JSON files.
    """
    print(f"Validating JSON files in: {base_path}\n")
    for file_name in os.listdir(base_path):
        if file_name.endswith(".json"):
            json_file = os.path.join(base_path, file_name)
            print(f"Checking: {json_file}")

            # Quick check: File exists and has content
            file_size = os.path.getsize(json_file)
            if file_size == 0:
                print("  ❌ Error: File is empty!")
                continue

            # Quick check: Line count
            with open(json_file, encoding="utf-8") as f:
                line_count = sum(1 for _ in f)
            print(f"  ✅ Line count: {line_count}")

            # Advanced check: JSON structure
            try:
                with open(json_file, encoding="utf-8") as f:
                    data = json.load(f)

                # Check for top-level structure (e.g., "nwt" key)
                if translation not in data:
                    print("  ❌ Error: Missing 'nwt' key in JSON structure!")
                else:
                    # Check for book name and content
                    books = data[translation]
                    if not books:
                        print("  ❌ Error: No books found in JSON!")
                    else:
                        for book_name, chapters in books.items():
                            print(f"  ✅ Book: {book_name}, Chapters: {len(chapters)}")

            except json.JSONDecodeError as e:
                print(f"  ❌ Error: Invalid JSON format! {e}")
            except Exception as e:
                print(f"  ❌ Error: Unexpected error: {e}")


def merge_and_sort_bible_files(input_dir, output_file, translation):
    """Merge and sort Bible JSON files into a single JSON."""
    merged_data = {translation: {}}

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_dir, file_name)
            try:
                with open(file_path, encoding="utf-8") as f:
                    book_data = json.load(f)
            except Exception as e:
                print(f"Error loading file {file_name}: {e}")
                continue

            for book, chapters in book_data.get(translation, {}).items():
                merged_data[translation].setdefault(book, {}).update(chapters)

    def sort_bible_data(bible_data):
        normalized_to_original = {
            book.replace("_", " ").lower(): book for book in bible_data
        }

        sorted_data = {}
        for book in BOOK_ORDER:
            normalized_name = book.lower()
            if normalized_name in normalized_to_original:
                original_name = normalized_to_original[normalized_name]
                sorted_data[original_name] = bible_data[original_name]

        return sorted_data

    sorted_data = sort_bible_data(merged_data[translation])
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({translation: sorted_data}, f, indent=4, ensure_ascii=False)

    print(f"Merged and sorted JSON files written to {output_file}")


def convert_all_books(input_dir, output_dir, translation="nwt-study"):
    """Parse and save Bible text files in a directory as JSON files."""
    os.makedirs(output_dir, exist_ok=True)

    normalized_book_order = {
        name.replace(" ", "_").lower(): name for name in BOOK_ORDER
    }

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".txt"):
            input_file = os.path.join(input_dir, file_name)
            raw_book_name = os.path.splitext(file_name)[0].lower()
            book_name = normalized_book_order.get(raw_book_name, raw_book_name)

            output_file = os.path.join(
                output_dir, f"{raw_book_name}.json"
            )  # Keep underscores

            # print(f"Processing: {input_file}")
            parsed_book = parse_book_to_json(input_file)

            # Save parsed JSON
            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(
                    {translation: {book_name: parsed_book}},
                    json_file,
                    indent=4,
                )
            # print(f"Saved JSON to: {output_file}")

    merge_and_sort_bible_files(
        output_dir, f"data/tmp/{translation}-bible.json", translation
    )


# Example usage
if __name__ == "__main__":
    input_dir = "data/bibles/jw_org/study"
    output_dir = "data/bibles/jw_org/study"
    convert_all_books(input_dir, output_dir, "nwt-study")
    validate_json_files(output_dir)
