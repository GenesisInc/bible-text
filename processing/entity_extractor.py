"""entity analysis"""

import json
from multiprocessing import Pool

import spacy

from utils import file_utils

# Load spaCy model
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


def extract_entities_from_verse(verse_text):
    """Extract named entities using spaCy."""
    doc = nlp(verse_text)
    return {
        "PERSON": [ent.text for ent in doc.ents if ent.label_ == "PERSON"],
        "DATE": [ent.text for ent in doc.ents if ent.label_ == "DATE"],
        "GPE": [ent.text for ent in doc.ents if ent.label_ == "GPE"],
    }


def extract_reference(bible_json_path, reference, translation):
    """Extracts text for a given Bible reference."""
    with open(bible_json_path, "r", encoding="utf-8") as file:
        bible_data = json.load(file)

    # Use the previously defined `get_bible_text` function
    return get_bible_text(reference, bible_data, translation)


def parse_reference(reference):
    """
    Parses a Bible reference string into book, chapter, and verse details.

    Special cases:
    - Single-chapter books (like Jude): Prefix "1:" to standalone verse numbers or ranges.
    """
    reference = reference.strip()
    if not reference:
        raise ValueError("Invalid reference format")

    # Step 1: Split by space to separate book and reference
    parts = reference.rsplit(" ", 1)
    if len(parts) == 1:
        # Only the book name is provided
        book = parts[0].lower()
        rest = ""
    else:
        book = parts[0].lower()
        rest = parts[1]  # This contains chapter:verse or a range

    # Step 2: Handle single-chapter books
    single_chapter_books = {"jude", "philemon", "2 john", "3 john"}
    if book in single_chapter_books:
        if "-" in rest:  # Range like "4-8"
            start, end = rest.split("-")
            if ":" not in start:
                start = f"1:{start}"  # Prefix chapter 1
            if ":" not in end:
                end = f"1:{end}"  # Prefix chapter 1
            rest = f"{start}-{end}"
        elif ":" not in rest:  # Single verse like "4"
            rest = f"1:{rest}"  # Prefix chapter 1

    return book, rest


def get_bible_text(reference, bible_data, translation):
    """Extracts Bible text based on a reference string."""
    try:
        book, verses = parse_reference(reference)
        if not verses:
            # Return the whole book
            return fetch_entire_book(bible_data, book)

        start_chapter, start_verse, end_chapter, end_verse = parse_verse_range(verses)
        return fetch_verses(
            bible_data,
            translation,
            book,
            start_chapter,
            start_verse,
            end_chapter,
            end_verse,
        )
    except KeyError as e:
        return f"Error: Missing key in Bible data - {str(e)}"
    except ValueError as e:
        return f"Error: Invalid reference format - {str(e)}"
    except TypeError as e:
        return f"Error: Type error encountered - {str(e)}"


def fetch_verses(
    bible_data, translation, book, start_chapter, start_verse, end_chapter, end_verse
):
    """Fetches verses across chapter and verse ranges."""
    result = []
    for chapter in range(start_chapter, end_chapter + 1):
        chapter_key = str(chapter)
        if chapter_key not in bible_data[translation].get(book, {}):
            continue

        verse_start = start_verse if chapter == start_chapter else 1
        verse_end = (
            end_verse
            if chapter == end_chapter
            else max(map(int, bible_data[translation][book][chapter_key].keys()))
        )

        for verse in range(verse_start, verse_end + 1):
            verse_key = str(verse)
            if verse_key in bible_data[translation][book][chapter_key]:
                result.append(bible_data[translation][book][chapter_key][verse_key])

    return " ".join(result)


def fetch_entire_book(bible_data, book):
    """Fetches all chapters and verses of a book."""
    result = []
    book_data = bible_data["nwt"].get(book, {})
    for chapter_key in sorted(book_data.keys(), key=int):
        chapter_data = book_data[chapter_key]
        for _, verse_text in sorted(chapter_data.items(), key=lambda x: int(x[0])):
            result.append(verse_text)
    return " ".join(result)


def parse_verse_range(verses):
    """Parses a verse range into start and end chapter/verse."""
    if "-" in verses:
        start, end = verses.split("-")
        start_chapter, start_verse = map(int, start.split(":"))
        if ":" in end:
            end_chapter, end_verse = map(int, end.split(":"))
        else:
            end_chapter = start_chapter
            end_verse = int(end)
    elif ":" in verses:
        start_chapter, start_verse = map(int, verses.split(":"))
        end_chapter, end_verse = start_chapter, start_verse
    else:
        start_chapter = int(verses)
        start_verse = 1
        end_chapter, end_verse = start_chapter, None
    return start_chapter, start_verse, end_chapter, end_verse


def load_bible_json(file_path):
    """Loads the Bible JSON data."""
    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def chapter_entities_analysis(chapter_data):
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
        chapter_entities_analysis(chapter_data),
    )


def perform_entity_analysis(
    bible_file,
    output_json_file,
    output_csv_file,
    translation="nwt",
    books=None,
):
    """Extracts entities and occupations from the Bible using multiprocessing."""
    # Step 1: Load Bible data
    bible_data = load_bible_json(bible_file)

    # Step 2: Prepare tasks for multiprocessing
    tasks = prepare_tasks(bible_data, translation, books)

    # Step 3: Process tasks in parallel
    results = process_tasks_parallel(tasks)

    # Step 4: Reorganize results into a nested JSON structure
    entities_and_occupations = reorganize_results(results)

    # Step 5: Save JSON output
    file_utils.save_to_json(entities_and_occupations, output_json_file)

    # Step 6: Save CSV output
    file_utils.save_to_csv(entities_and_occupations, output_csv_file)


def prepare_tasks(bible_data, translation, books):
    """Prepares tasks for multiprocessing."""
    return [
        (book, chapter_num, chapter_data)
        for book, chapters in bible_data[translation].items()
        if not books or book in books
        for chapter_num, chapter_data in chapters.items()
    ]


def process_tasks_parallel(tasks):
    """Processes tasks in parallel using multiprocessing."""
    with Pool() as pool:
        return pool.map(process_chapter, tasks)


def reorganize_results(results):
    """Reorganizes the results into a nested JSON structure."""
    entities_and_occupations = {}
    for book, chapter_num, chapter_data in results:
        if book not in entities_and_occupations:
            entities_and_occupations[book] = {}
        entities_and_occupations[book][chapter_num] = chapter_data
    return entities_and_occupations
