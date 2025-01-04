# bible-text/core/translation_loader/nwt_study.py
import json
import os


def parse_bible_to_json(filename, chapter_sep=" ", verse_sep=" "):
    """Parse Bible text into a structured JSON format, supporting single-chapter books.

    Args:
        filename (str): Path to the text file containing the Bible book.
        chapter_sep (str): Character(s) indicating the start of a chapter.
        verse_sep (str): Character(s) indicating the start of a verse.

    Returns:
        dict: JSON structure of the parsed Bible text.
    """
    result = {"1": {}}  # Default to chapter "1" for single-chapter books
    current_chapter = "1"
    current_verse = None

    with open(filename, encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Detect chapters (only for multi-chapter books)
            if chapter_sep in line and line.split(chapter_sep, 1)[0].isdigit():
                chapter_number, remaining_text = line.split(chapter_sep, 1)
                current_chapter = chapter_number.strip()
                result[current_chapter] = {}
                current_verse = None  # Reset verse
                line = remaining_text.strip()

            # Detect verses
            if verse_sep in line and line.split(verse_sep, 1)[0].isdigit():
                verse_number, verse_text = line.split(verse_sep, 1)
                current_verse = verse_number.strip()
                result[current_chapter][current_verse] = verse_text.strip()
                continue

            # Handle multi-line verses (append to the last detected verse)
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


def merge_and_sort_bible_files(input_dir, output_file, translation):  # noqa: C901
    """Merge all Bible JSON files in a directory into a single JSON."""

    def save_to_json_local(data, file_path):
        """Local function to save JSON data."""
        try:
            print(f"Writing data to {file_path} with {len(data)} top-level keys.")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Data successfully written to {file_path}")
        except Exception as e:
            print(f"Error writing JSON to {file_path}: {e}")

    merged_data = {translation: {}}

    # Merge JSON files
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_dir, file_name)
            try:
                with open(file_path, encoding="utf-8") as f:
                    book_data = json.load(f)
            except Exception as e:
                print(f"Error loading file {file_name}: {e}")
                continue

            if translation not in book_data:
                print(f"Skipping file {file_name}: Missing key '{translation}'")
                continue

            # Proper merging
            for book, chapters in book_data[translation].items():
                if book not in merged_data[translation]:
                    merged_data[translation][book] = chapters
                else:
                    merged_data[translation][book].update(chapters)

    print(f"Total books in merged_data[{translation}]: {len(merged_data[translation])}")

    # Sort the data locally
    def sort_bible_data_local(bible_data):
        """Sort Bible data by a predefined order."""
        from config.book_order import BOOK_ORDER  # Ensure this is accessible

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

    # Sort the merged data
    sorted_data = sort_bible_data_local(merged_data[translation])

    # Save sorted data
    save_to_json_local({translation: sorted_data}, output_file)

    print(f"Merged and sorted JSON files written to {output_file}")


def convert_all_books(input_dir, output_dir, translation="nwt-study"):
    """Parse all Bible text files in the specified directory and save as JSON.

    Args:
        input_dir (str): Path to the directory containing text files.
    """
    # Ensure output directory exists
    output_dir = input_dir
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over all .txt files in the input_dir
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".txt"):
            input_file = os.path.join(input_dir, file_name)
            book_name = os.path.splitext(file_name)[0]  # Strip extension
            output_file = os.path.join(output_dir, f"{book_name}.json")

            print(f"Processing: {input_file}")
            parsed_bible = parse_bible_to_json(input_file)

            # Save the parsed JSON
            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(
                    {translation: {book_name.lower(): parsed_bible}},
                    json_file,
                    indent=4,
                )
            print(f"Saved JSON to: {output_file}")

    merge_and_sort_bible_files(output_dir, f"{translation}-bible.json", translation)


# Example usage
if __name__ == "__main__":
    input_dir = "data/bibles/jw_org/study"
    output_dir = "data/bibles/jw_org/study"
    convert_all_books(input_dir, output_dir, "nwt-study")
    validate_json_files(output_dir)
