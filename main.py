import os
import spacy
import json
import csv
import unicodedata

# Load spaCy's English NLP model
nlp = spacy.load("en_core_web_sm")

# Base path of the Bible text organized by book and chapter
base_path = "newWorldTranslation/english/2013-release"


def normalize_unicode(text):
    """Convert Unicode characters to ASCII equivalents where possible."""
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def process_word_by_word(words, output_path):
    """Processes each word individually to extract entities."""
    entities = {
        "PERSON": set(),
        "GPE": set(),
        "TIME": set(),
        "LAW": set(),
        "EVENT": set(),
    }

    for word in words:
        doc = nlp(word)
        for ent in doc.ents:
            if ent.label_ in entities:
                # Normalize Unicode characters
                entities[ent.label_].add(normalize_unicode(ent.text))

    # Write results to output files by entity type
    for entity_type, entity_words in entities.items():
        with open(f"{output_path}.{entity_type}", "w") as f:
            for entity in sorted(entity_words):
                f.write(f"{entity}\n")


def process_large_text(text, book, chapter, results):
    """Processes a larger text block (e.g., a whole chapter) to extract entities."""
    doc = nlp(text)
    entities = {"PERSON": {}, "GPE": {}, "TIME": {}, "LAW": {}, "EVENT": {}}

    # Extract entities and count occurrences
    for ent in doc.ents:
        if ent.label_ in entities:
            # Normalize Unicode characters
            entity_name = normalize_unicode(ent.text)
            entities[ent.label_][entity_name] = (
                entities[ent.label_].get(entity_name, 0) + 1
            )

    # Store results in nested dictionary structure
    if book not in results:
        results[book] = {}
    results[book][chapter] = entities


def process_bible_text(base_path):
    results = {}

    for book in sorted(os.listdir(base_path)):
        book_path = os.path.join(base_path, book)
        if os.path.isdir(book_path):
            for chapter in sorted(os.listdir(book_path)):
                chapter_path = os.path.join(book_path, chapter)
                if os.path.isfile(chapter_path):
                    # Read chapter text
                    with open(chapter_path, "r") as file:
                        text = file.read().strip()

                    # Process the chapter as a large text block
                    process_large_text(text, book, chapter, results)

    return results


def save_to_json(results, output_path):
    """Saves the results to a JSON file with ASCII-only text."""
    with open(output_path, "w") as json_file:
        json.dump(results, json_file, indent=2, ensure_ascii=True)


def save_to_csv(results, output_path):
    """Saves the results to a CSV file."""
    with open(output_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Book", "Chapter", "Entity_Type", "Entity_Name", "Count"])

        for book, chapters in results.items():
            for chapter, entities in chapters.items():
                for entity_type, names in entities.items():
                    for name, count in names.items():
                        writer.writerow([book, chapter, entity_type, name, count])


def save_to_flattened_csv(results, output_path):
    """Saves the results to a flattened CSV file with each chapter in a single line."""
    with open(output_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Book", "Chapter", "PERSON", "GPE", "TIME", "LAW", "EVENT"])

        for book, chapters in results.items():
            for chapter, entities in chapters.items():
                # Flatten entity counts by type
                person_count = sum(entities["PERSON"].values())
                gpe_count = sum(entities["GPE"].values())
                time_count = sum(entities["TIME"].values())
                law_count = sum(entities["LAW"].values())
                event_count = sum(entities["EVENT"].values())

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
    # Output paths for JSON and CSV
    output_json = "analysis/entities.json"
    output_csv = "analysis/entities.csv"
    output_flattened_csv = "analysis/chapter-entity-summary.csv"

    # Run processing and save results in JSON and CSV formats
    results = process_bible_text(base_path)
    save_to_json(results, output_json)
    save_to_csv(results, output_csv)
    save_to_flattened_csv(results, output_flattened_csv)

    print("Processing complete! Results saved to JSON and CSV files.")


if __name__ == "__main__":
    main()
