""" search engine """

import sys
import csv
import json
import re


def find_matches(bible_json_path, phrase, top_n=10, output_csv=False):
    """Find top matches for a phrase in Bible text."""
    with open(bible_json_path, "r", encoding="utf-8") as file:
        bible_data = json.load(file)

    # Normalize input
    phrase = phrase.strip().lower()  # Trim spaces and normalize case

    # Regex for part-of-word or multi-word search
    regex = rf"{re.escape(phrase)}"  # Match substring, regardless of single or multiple words

    matches = []
    for book, chapters in bible_data["nwt"].items():
        for chapter, verses in chapters.items():
            for verse, text in verses.items():
                # Match based on regex
                if re.search(regex, text, re.IGNORECASE):
                    matches.append(
                        {"book": book, "chapter": chapter, "verse": verse, "text": text}
                    )

    # Total matches
    total_matches = len(matches)

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

        # Print summary to stderr to separate it from CSV output
        print(
            f"Showing top {len(sorted_matches)} of {total_matches} matches",
            file=sys.stderr,
        )
    else:
        print(f"Showing top {len(sorted_matches)} of {total_matches} matches")
        return sorted_matches
