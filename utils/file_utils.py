""" file utils"""

import json

from config.book_order import BOOK_ORDER


def save_to_json(data, output_file):
    """Save data to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"data successfully written to {output_file}")


def load_from_json(input_file):
    """Load data from a JSON file."""
    with open(input_file, "r", encoding="utf-8") as f:
        return json.load(f)


def sort_and_save(data, output_file):
    """Save hierarchical data to a JSON file."""
    save_to_json(sort_bible_data(data), output_file)


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
