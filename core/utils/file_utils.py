""" file utils"""

import csv
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


def save_to_csv(entities_and_occupations, output_csv_file):
    """Saves entities and occupations data to a CSV file."""
    with open(output_csv_file, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Book", "Chapter", "Verse", "Type", "Text"])
        for book, chapters in entities_and_occupations.items():
            for chapter, verses in chapters.items():
                for verse, data in verses.items():
                    # Save entities
                    for entity_type, entity_texts in data["entities"].items():
                        for entity_text in entity_texts:
                            writer.writerow(
                                [book, chapter, verse, entity_type, entity_text]
                            )
                    # Save occupations
                    for occupation in data["occupations"]:
                        writer.writerow(
                            [book, chapter, verse, "OCCUPATION", occupation]
                        )
    print(f"CSV results saved to {output_csv_file}")
