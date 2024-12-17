"""extract few entities from bible"""

import argparse
import csv
import json
import os
import re
import unicodedata
from pathlib import Path

import spacy

# Load spaCy's English NLP model
nlp = spacy.load("en_core_web_sm")

# Constants
OUTPUT_DIR = Path("analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BASE_PATH = "../newWorldTranslation/english/2013-release"

LIFESPAN_INDICATORS = {"lived for", "was", "amounted to", "were", "to be"}
EXCLUSION_KEYWORDS = {"reigned", "gathered to", "length of", "satisfied with years"}


def normalize_unicode(text):
    """Cleans up Unicode characters, standardizes spaces, and trims around punctuation."""
    # Define replacements in a dictionary for flexibility and readability
    replacements = {
        "\u00A0": " ",  # Non-breaking space to regular space
        "\n": " ",  # Newline to space
        "\u2019": "'",  # Right single quotation mark to apostrophe
        "\u02b9": "",  # Modifier letter prime (remove)
        "\u00b7": "",  # Middle dot (remove)
    }

    # Apply replacements using the dictionary
    for unicode_char, replacement in replacements.items():
        text = text.replace(unicode_char, replacement)

    # Normalize to ASCII, removing accents and other diacritics
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

    # Remove extra spaces around punctuation and collapse multiple spaces
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)  # Remove space before punctuation
    text = re.sub(r"\s{2,}", " ", text).strip()  # Collapse multiple spaces to single

    return text


def extract_context(text, start, end):
    """Extracts context around an entity, retaining possessives and
    handling contractions correctly."""
    # Tokenize using spaCy to retain possessives
    doc = nlp(text)
    words = [token.text for token in doc]

    # If possessive "'s" precedes the entity, adjust start to include it
    if start > 0 and words[start - 1] == "'s":
        start -= 1  # Include possessive "'s" in context

    # Capture 3 words before and after the entity for full context
    entity_words = words[start:end]
    before = " ".join(words[max(0, start - 3) : start])
    after = " ".join(words[end : end + 3])

    # Join context and ensure spaces are clean
    context = f"{before} {' '.join(entity_words)} {after}".strip()
    context = re.sub(r"\s{2,}", " ", context)  # Collapse extra spaces

    return context


def get_reference(book, chapter, verse_num):
    """Generates a verse reference in 'Book Chapter:Verse' format."""
    book_name = book.split("-")[1]
    return f"{book_name} {int(chapter)}:{verse_num}"


def traverse_bible_text(base_path):
    """Yields each chapter text along with book and chapter info."""
    for book in sorted(os.listdir(base_path)):
        book_path = os.path.join(base_path, book)
        if os.path.isdir(book_path):
            for chapter in sorted(os.listdir(book_path)):
                chapter_path = os.path.join(book_path, chapter)
                if os.path.isfile(chapter_path):
                    with open(chapter_path, "r", encoding="utf-8") as file:
                        yield book, chapter, file.read().strip()


def extract_entities_from_verse(verse_text, verse_num, entities, book, chapter):
    """Extracts entities from verse text and updates the entities dictionary."""
    doc = nlp(verse_text)
    reference = get_reference(book, chapter, verse_num)

    for ent in doc.ents:
        if ent.label_ in entities:
            entity_name = normalize_unicode(ent.text)
            entity_data = entities[ent.label_].setdefault(
                entity_name, {"Count": 0, "Context": []}
            )
            entity_data["Count"] += 1

            # Generate context and normalize for final output
            context_text = extract_context(verse_text, ent.start, ent.end)
            entity_data["Context"].append(
                {
                    "Reference": reference,
                    "Text": normalize_unicode(context_text),
                }
            )


def process_large_text(text, book, chapter, results):
    """Processes a larger text block to extract entities with context."""
    entities = {"PERSON": {}, "GPE": {}, "TIME": {}, "LAW": {}, "EVENT": {}}
    lines = text.splitlines()
    verse_pattern = r"(\d+)\u00A0"

    for line in lines:
        verse_boundaries = [
            (m.start(), m.group(1)) for m in re.finditer(verse_pattern, line)
        ]
        verse_boundaries.append((len(line), None))

        for i, (start_idx, verse_num) in enumerate(verse_boundaries[:-1]):
            verse_text = line[start_idx : verse_boundaries[i + 1][0]].strip()
            extract_entities_from_verse(verse_text, verse_num, entities, book, chapter)

    results.setdefault(book, {})[chapter] = entities


def detect_lifespan_phrases(chapter_text, book="Genesis", chapter="16"):
    """Detects phrases indicating a person's lifespan with correct verse
    references and confidence scores."""
    # Pattern to identify verse markers (e.g., "1 ", "2 ", etc., followed by a non-breaking space)
    verse_pattern = r"(\d+)\u00A0"
    lifespans_dict = {}

    # Find verse boundaries using the pattern
    verse_matches = list(re.finditer(verse_pattern, chapter_text))
    for i, match in enumerate(verse_matches):
        verse_num = match.group(1)
        start_idx = match.end()
        end_idx = (
            verse_matches[i + 1].start()
            if i + 1 < len(verse_matches)
            else len(chapter_text)
        )

        verse_text = normalize_unicode(chapter_text[start_idx:end_idx].strip())
        reference = get_reference(book, chapter, verse_num)

        # Process the verse text for lifespan phrases
        doc = nlp(verse_text)
        person, years = None, None

        for ent in doc.ents:
            if ent.label_ == "PERSON":
                person = ent.text
            elif ent.label_ in {"CARDINAL", "DATE"}:
                years = extract_numeric_value(ent.text)
                if years and person:  # Ensure both person and years are available
                    confidence = calculate_confidence(verse_text.lower())
                    if confidence > 0:
                        lifespan_data = lifespans_dict.setdefault(person, [])
                        lifespan_data.append(
                            {
                                "Explicit Lifespan": years,
                                "Confidence": round(confidence, 2),
                                "Context": {"Reference": reference, "Text": verse_text},
                            }
                        )

    return lifespans_dict


def calculate_confidence(sentence_text):
    """Calculates confidence based on lifespan indicators and exclusion keywords."""
    indicator_matches = sum(
        1 for phrase in LIFESPAN_INDICATORS if phrase in sentence_text
    )
    exclusion_matches = sum(1 for excl in EXCLUSION_KEYWORDS if excl in sentence_text)
    return (
        indicator_matches / (indicator_matches + 1)
        if indicator_matches > 0 and exclusion_matches == 0
        else 0
    )


def extract_numeric_value(verse_text):
    """Extracts a numeric value from verse_text if it’s purely numeric."""
    numeric_text = re.sub(r"[^\d]", "", verse_text)
    return int(numeric_text) if numeric_text.isdigit() else None


def process_entities(base_path):
    """Process entities and save results."""
    results = {}
    for book, chapter, text in traverse_bible_text(base_path):
        process_large_text(text, book, chapter, results)
    save_results(results, "entities")


def process_lifespan(base_path):
    """Process lifespan statements and save results."""
    lifespans = {}
    for book, chapter, text in traverse_bible_text(base_path):
        chapter_lifespans = detect_lifespan_phrases(text, book, chapter)
        if chapter_lifespans:
            lifespans.setdefault(book, {})[chapter] = chapter_lifespans
    save_results(lifespans, "lifespans")


def save_results(data, data_type):
    """Saves results to JSON and CSV files based on data type."""
    json_path = OUTPUT_DIR / f"{data_type}.json"
    csv_path = OUTPUT_DIR / f"{data_type}.csv"

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=True)

    if data_type == "entities":
        with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
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
            for book, chapters in data.items():
                for chapter, entities in chapters.items():
                    for entity_type, names in entities.items():
                        for name, entity_data in names.items():
                            for context in entity_data["Context"]:
                                writer.writerow(
                                    [
                                        book,
                                        chapter,
                                        entity_type,
                                        name,
                                        entity_data["Count"],
                                        context["Reference"],
                                        context["Text"],
                                    ]
                                )


def main():
    """Main function with CLI options for entity tagging or lifespan extraction."""
    parser = argparse.ArgumentParser(
        description="Process Bible text for entity tagging or lifespan extraction."
    )
    parser.add_argument(
        "--tag-entities", action="store_true", help="Run entity tagging on Bible text."
    )
    parser.add_argument(
        "--extract-lifespan",
        action="store_true",
        help="Run lifespan extraction on Bible text.",
    )
    args = parser.parse_args()

    if args.tag_entities:
        process_entities(BASE_PATH)
    elif args.extract_lifespan:
        process_lifespan(BASE_PATH)
    else:
        print("Please specify an action with --tag-entities or --extract-lifespan")


if __name__ == "__main__":
    main()
