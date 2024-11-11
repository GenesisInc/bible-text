"""module nlp"""

import csv
import json
import os
import re
import unicodedata

import spacy

# Load spaCy's English NLP model
nlp = spacy.load("en_core_web_sm")


def normalize_unicode(text):
    """Removes specific unwanted Unicode characters and trims extra spaces around punctuation."""
    # Step 1: Replace non-breaking spaces (U+00A0) with nothing
    text = text.replace("\u00A0", "")

    # Step 2: Normalize text to ASCII (removing other unwanted Unicode characters)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

    # Step 3: Remove spaces directly before punctuation (e.g., before commas, periods)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)

    # Step 4: Remove any double spaces that may remain
    return re.sub(r"\s{2,}", " ", text).strip()


def extract_context(words, start, end):
    """Extracts up to 3 words before and after an entity."""
    entity_words = words[start:end]
    # Get up to 3 words before and after
    before = " ".join(words[max(0, start - 3) : start])
    after = " ".join(words[end : end + 3])
    return f"{before} {' '.join(entity_words)} {after}".strip()


def process_large_text(text, book, chapter, results):
    """Processes a larger text block (e.g., a whole chapter) to extract entities with context."""
    entities = {"PERSON": {}, "GPE": {}, "TIME": {}, "LAW": {}, "EVENT": {}}

    # Split text by lines and locate verses within each line
    lines = text.splitlines()
    verse_pattern = (
        r"(\d+)\u00A0"  # Pattern to identify verse numbers followed by U+00A0
    )

    for line in lines:
        verse_boundaries = find_verse_boundaries(line, verse_pattern)

        for start_idx, verse_num, end_idx in verse_boundaries:
            verse_text = line[start_idx:end_idx].strip()
            extract_entities_from_verse(verse_text, verse_num, entities)

    # Store results
    if book not in results:
        results[book] = {}
    results[book][chapter] = entities


def find_verse_boundaries(line, pattern):
    """Finds start and end positions of each verse in a line."""
    verse_boundaries = [(m.start(), m.group(1)) for m in re.finditer(pattern, line)]
    verse_boundaries.append(
        (len(line), None)
    )  # Mark the end of the line as the last boundary

    # Create tuples of (start_idx, verse_num, end_idx) for each verse
    return [
        (verse_boundaries[i][0], verse_boundaries[i][1], verse_boundaries[i + 1][0])
        for i in range(len(verse_boundaries) - 1)
    ]


def extract_entities_from_verse(verse_text, verse_num, entities):
    """Extracts entities from verse text, captures context, and updates the entities dictionary."""
    doc = nlp(verse_text)
    for ent in doc.ents:
        if ent.label_ in entities:
            update_entity_context(ent, verse_num, entities[ent.label_])


def update_entity_context(ent, verse_num, entity_dict):
    """Normalizes the entity, updates count, and adds context with verse number."""
    entity_name = normalize_unicode(ent.text)

    # Initialize entity entry if it doesn't exist
    if entity_name not in entity_dict:
        entity_dict[entity_name] = {"Count": 0, "Context": []}

    # Increment count
    entity_dict[entity_name]["Count"] += 1

    # Capture context and normalize to remove unwanted Unicode
    context_text = extract_context(
        [token.text for token in ent.doc], ent.start, ent.end
    )
    normalized_context_text = normalize_unicode(context_text)

    # Add context with verse number
    entity_dict[entity_name]["Context"].append(
        {"Verse": int(verse_num), "Text": normalized_context_text}
    )


def process_bible_text(base_path):
    """process_bible_text"""
    results = {}

    for book in sorted(os.listdir(base_path)):
        book_path = os.path.join(base_path, book)
        if os.path.isdir(book_path):
            for chapter in sorted(os.listdir(book_path)):
                chapter_path = os.path.join(book_path, chapter)
                if os.path.isfile(chapter_path):
                    # Read chapter text
                    with open(chapter_path, "r", encoding="utf-8") as file:
                        text = file.read().strip()

                    # Process the chapter as a large text block
                    process_large_text(text, book, chapter, results)

    return results


def save_to_json(results, output_path):
    """Saves the results to a JSON file with ASCII-only text."""
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(results, json_file, indent=2, ensure_ascii=True)


def save_to_csv(results, output_path):
    """Saves the results to a CSV file."""
    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "Book",
                "Chapter",
                "Entity_Type",
                "Entity_Name",
                "Count",
                "Verse",
                "Context",
            ]
        )

        for book, chapters in results.items():
            for chapter, entities in chapters.items():
                for entity_type, names in entities.items():
                    for name, data in names.items():
                        for context in data["Context"]:
                            writer.writerow(
                                [
                                    book,
                                    chapter,
                                    entity_type,
                                    name,
                                    data["Count"],
                                    context["Verse"],
                                    context["Text"],
                                ]
                            )


def save_to_flattened_csv(results, output_path):
    """Saves the results to a flattened CSV file with each chapter in a single line."""
    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Book", "Chapter", "PERSON", "GPE", "TIME", "LAW", "EVENT"])

        for book, chapters in results.items():
            for chapter, entities in chapters.items():
                # Flatten entity counts by type
                person_count = sum(
                    entity["Count"] for entity in entities["PERSON"].values()
                )
                gpe_count = sum(entity["Count"] for entity in entities["GPE"].values())
                time_count = sum(
                    entity["Count"] for entity in entities["TIME"].values()
                )
                law_count = sum(entity["Count"] for entity in entities["LAW"].values())
                event_count = sum(
                    entity["Count"] for entity in entities["EVENT"].values()
                )

                # Write a single row per chapter with counts by entity type
                writer.writerow(
                    [
                        book,
                        chapter,
                        person_count,
                        gpe_count,
                        time_count,
                        law_count,
                        event_count,
                    ]
                )


def main():
    """main"""
    # Output paths for JSON and CSV
    output_json = "analysis/entities.json"
    output_csv = "analysis/entities.csv"
    output_flattened_csv = "analysis/chapter-entity-summary.csv"

    # Base path of the Bible text organized by book and chapter
    base_path = "newWorldTranslation/english/2013-release"

    # Run processing and save results in JSON and CSV formats
    results = process_bible_text(base_path)
    save_to_json(results, output_json)
    save_to_csv(results, output_csv)
    save_to_flattened_csv(results, output_flattened_csv)

    print("Processing complete! Results saved to JSON and CSV files.")


if __name__ == "__main__":
    main()
