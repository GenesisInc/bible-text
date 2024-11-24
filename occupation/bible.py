"""process bible text"""

import argparse
import csv
import json
import os
import re
import sys
import unicodedata
from multiprocessing import Pool

import spacy

# Load spaCy's English model with only the NER component
nlp = spacy.load("en_core_web_sm", disable=["parser"])

# Occupation keywords for matching
occupation_keywords = {
    "apothecary",
    "architect",
    "armor maker",
    "armor-bearer",
    "astrologer",
    "astronomer",
    "baker",
    "beggar",
    "blacksmith",
    "builder of city walls",
    "camel driver",
    "caretaker of sacred items",
    "carpenter",
    "charioteer",
    "chief of army",
    "choir member",
    "cook",
    "cupbearer",
    "cupmaker",
    "dancer",
    "dealer in purple cloth",
    "dyer",
    "elder",
    "executioner",
    "farmer",
    "fisher",
    "fisherman",
    "flock herder",
    "gatekeeper",
    "goldsmith",
    "governor",
    "harvester",
    "herder",
    "high priest",
    "horseman",
    "hunter",
    "judge",
    "king",
    "lawyer",
    "linen worker",
    "mason",
    "merchant",
    "metalworker",
    "midwife",
    "miller",
    "musician",
    "perfumer",
    "physician",
    "potter",
    "priest’s assistant",
    "priest",
    "prophet",
    "queen",
    "sandal maker",
    "scout",
    "scribe",
    "servant",
    "shepherd",
    "shipbuilder",
    "shipmaster",
    "singer",
    "slave",
    "slavegirl",
    "soldier",
    "spy",
    "stonecutter",
    "tax collector",
    "teacher",
    "temple servant",
    "tent weaver",
    "tent-dweller",
    "tentmaker",
    "trader",
    "vineyard keeper",
    "weaver",
    "winemaker",
}


def extract_reference(bible_json_path, reference):
    """Extracts text for a given Bible reference."""
    with open(bible_json_path, "r", encoding="utf-8") as file:
        bible_data = json.load(file)

    # Use the previously defined `get_bible_text` function
    return get_bible_text(reference, bible_data)


def get_bible_text(reference, bible_data):
    """Extracts Bible text based on a reference string."""
    try:
        parts = reference.lower().split(" ")
        book = parts[0]
        verses = parts[1]

        if "-" in verses:
            start, end = verses.split("-")
            start_chapter, start_verse = map(int, start.split(":"))
            if ":" in end:
                end_chapter, end_verse = map(int, end.split(":"))
            else:
                end_chapter = start_chapter
                end_verse = int(end)
        else:
            start_chapter, start_verse = map(int, verses.split(":"))
            end_chapter, end_verse = start_chapter, start_verse

        result = []
        for chapter in range(start_chapter, end_chapter + 1):
            chapter_key = str(chapter)
            if chapter_key not in bible_data["nwt"][book]:
                continue

            if chapter == start_chapter:
                verse_start = start_verse
            else:
                verse_start = 1

            if chapter == end_chapter:
                verse_end = end_verse
            else:
                verse_end = max(map(int, bible_data["nwt"][book][chapter_key].keys()))

            for verse in range(verse_start, verse_end + 1):
                verse_key = str(verse)
                if verse_key in bible_data["nwt"][book][chapter_key]:
                    result.append(bible_data["nwt"][book][chapter_key][verse_key])

        return " ".join(result)

    except KeyError as e:
        return f"Error: Missing key in Bible data - {str(e)}"
    except ValueError as e:
        return f"Error: Invalid reference format - {str(e)}"
    except TypeError as e:
        return f"Error: Type error encountered - {str(e)}"


# Text cleaning function
def clean_text(text):
    """Cleans text by removing non-ASCII characters, normalizing unicode,
    and adding spaces where needed."""
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


# Extract entities and occupations from a single verse
def extract_entities_from_verse(verse_text):
    """Extracts named entities from a verse using spaCy's NER model."""
    doc = nlp(verse_text)
    entities = {"PERSON": [], "DATE": [], "GPE": [], "ORG": [], "NORP": []}
    for ent in doc.ents:
        stripped_text = ent.text.strip()
        if ent.label_ == "PERSON" and stripped_text[0].isupper():
            entities["PERSON"].append(stripped_text)
        elif ent.label_ == "PERSON":
            print(f"Lowercase PERSON entity skipped: '{stripped_text}'")
        elif ent.label_ in entities:
            entities[ent.label_].append(stripped_text)
    return entities


def extract_occupations_from_verse(verse_text):
    """Extracts occupation-related terms from a verse based on predefined keywords."""
    doc = nlp(verse_text)
    occupations = [
        token.text.lower() for token in doc if token.lemma_ in occupation_keywords
    ]
    return occupations


def extract_entities_and_occupations_from_chapter(chapter_data):
    """Extracts entities and occupations for all verses in a chapter."""
    chapter_entities = {
        verse_num: {
            "entities": {"PERSON": [], "DATE": [], "GPE": [], "ORG": [], "NORP": []},
            "occupations": [],
        }
        for verse_num in chapter_data
    }

    # Process each verse in the chapter
    for verse_num, doc in zip(
        chapter_data.keys(), nlp.pipe(chapter_data.values(), batch_size=50)
    ):
        for ent in doc.ents:
            # Extract named entities
            if ent.label_ == "PERSON" and ent.text.strip()[0].isupper():
                chapter_entities[verse_num]["entities"]["PERSON"].append(
                    ent.text.strip()
                )
            elif ent.label_ in chapter_entities[verse_num]["entities"]:
                chapter_entities[verse_num]["entities"][ent.label_].append(
                    ent.text.strip()
                )

        # Extract occupations (use lemma to ensure consistent forms)
        occupations = [
            token.lemma_ for token in doc if token.lemma_ in occupation_keywords
        ]
        chapter_entities[verse_num]["occupations"].extend(occupations)

    return chapter_entities


# Multiprocessing-friendly wrapper for chapter processing
def process_chapter(args):
    """Processes a single chapter for multiprocessing."""
    book, chapter_num, chapter_data = args
    return (
        book,
        chapter_num,
        extract_entities_and_occupations_from_chapter(chapter_data),
    )


def perform_entity_extraction(
    bible_file, output_json_file, output_csv_file, books=None
):
    """Extracts entities and occupations from the Bible using multiprocessing."""
    bible_data = load_bible_json(bible_file)

    # Prepare tasks for multiprocessing
    tasks = [
        (book, chapter_num, chapter_data)
        for book, chapters in bible_data["nwt"].items()
        if not books or book in books
        for chapter_num, chapter_data in chapters.items()
    ]

    # Process chapters in parallel
    with Pool() as pool:
        results = pool.map(process_chapter, tasks)

    # Reorganize results into nested JSON structure
    entities_and_occupations = {}
    for book, chapter_num, chapter_data in results:
        if book not in entities_and_occupations:
            entities_and_occupations[book] = {}
        entities_and_occupations[book][chapter_num] = chapter_data

    # Save JSON output
    with open(output_json_file, "w", encoding="utf-8") as json_file:
        json.dump(entities_and_occupations, json_file, indent=4)
    print(
        f"Entity and occupation extraction complete. JSON results saved to {output_json_file}"
    )

    # Save CSV output
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


def load_bible_json(file_path):
    """Loads the Bible JSON data."""
    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def generate_bible_json(base_path, output_file):
    """Generates a structured JSON representation of Bible text files."""
    bible_data = {"nwt": {}}
    verse_pattern = r"(\d+)\u00A0"

    for book_folder in sorted(os.listdir(base_path)):
        book_path = os.path.join(base_path, book_folder)
        if os.path.isdir(book_path):
            book_name = book_folder.split("-", 1)[1].lower()
            bible_data["nwt"][book_name] = {}
            for chapter_file in sorted(os.listdir(book_path)):
                chapter_path = os.path.join(book_path, chapter_file)
                if os.path.isfile(chapter_path) and chapter_file.isdigit():
                    chapter_number = int(chapter_file)
                    bible_data["nwt"][book_name][str(chapter_number)] = {}
                    with open(chapter_path, "r", encoding="utf-8") as file:
                        text = file.read()
                        verses = re.split(verse_pattern, text)
                        for i in range(1, len(verses), 2):
                            verse_number = verses[i]
                            verse_text = clean_text(verses[i + 1].strip())
                            bible_data["nwt"][book_name][str(chapter_number)][
                                verse_number
                            ] = verse_text

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(bible_data, json_file, indent=4)
    print(f"Bible data successfully written to {output_file}")


def find_matches(bible_json_path, phrase, top_n=10, output_csv=False):
    """Find top matches for a phrase in Bible text and optionally output as CSV."""
    with open(bible_json_path, "r", encoding="utf-8") as file:
        bible_data = json.load(file)

    # Normalize phrase for case-insensitive search
    phrase = phrase.lower()
    matches = []

    for book, chapters in bible_data["nwt"].items():
        for chapter, verses in chapters.items():
            for verse, text in verses.items():
                # Case-insensitive match using regex
                if re.search(rf"\b{re.escape(phrase)}\b", text, re.IGNORECASE):
                    matches.append(
                        {"book": book, "chapter": chapter, "verse": verse, "text": text}
                    )

    # Sort and limit matches
    sorted_matches = sorted(matches, key=lambda x: len(x["text"]))[:top_n]

    if output_csv:
        # Write to stdout as CSV
        writer = csv.DictWriter(
            sys.stdout,
            fieldnames=["book", "chapter", "verse", "text"],
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        writer.writerows(sorted_matches)
    else:
        return sorted_matches


def main():
    """Main function to handle CLI."""
    parser = argparse.ArgumentParser(
        description="Process Bible text and extract entities."
    )
    parser.add_argument(
        "--generate", action="store_true", help="Generate Bible JSON from text files"
    )
    parser.add_argument(
        "--extract", action="store_true", help="Extract entities from Bible JSON"
    )
    parser.add_argument(
        "--reference",
        type=str,
        help="Provide a Bible reference (e.g., 'Gen 1:1', 'Gen 1:10-2:3')",
    )
    parser.add_argument(
        "--match",
        type=str,
        help="Find matches for a phrase in the Bible text",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        help="Number of top matches to display",
        default=10,  # Default to 10 if not provided
    )
    parser.add_argument(
        "--base-path",
        type=str,
        help="Base path of Bible text files",
        default="../newWorldTranslation/english/2013-release",
    )
    parser.add_argument(
        "--bible-json",
        type=str,
        help="Path to the Bible JSON file for entity extraction",
        default="data/bible_data.json",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        help="Output JSON file path",
        default="data/bible_entities.json",
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        help="Output CSV file path",
        default="data/bible_entities.csv",
    )
    parser.add_argument(
        "--books",
        type=str,
        nargs="*",
        help="Specify one or more books to extract (e.g., genesis exodus)",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Output the results in CSV format",
    )

    args = parser.parse_args()

    if args.generate:
        generate_bible_json(args.base_path, args.bible_json)
    elif args.extract:
        perform_entity_extraction(
            args.bible_json, args.output_json, args.output_csv, books=args.books
        )
    elif args.reference:
        result = extract_reference(args.bible_json, args.reference)
        print(result)
    elif args.match:
        matches = find_matches(
            args.bible_json, args.match, top_n=args.top_n, output_csv=args.csv
        )
        if not args.csv:
            for match in matches:
                print(
                    f"{match['book']} {match['chapter']}:{match['verse']} - {match['text']}"
                )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
