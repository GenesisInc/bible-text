"""main"""

import argparse
import json

from extraction import bible_extractor, manipulator, nwt_extractor
from processing import entity_extractor, search_engine


def main():
    """Main function to handle CLI."""
    parser = argparse.ArgumentParser(
        description="CLI to process Bible text, extract entities, and perform searches."
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Sub-command for loading NWT to JSON
    nwt_parser = subparsers.add_parser(
        "load-nwt",
        help="Load New World Translation (NWT) data into JSON format.",
    )
    nwt_parser.add_argument(
        "--base-path",
        type=str,
        default="newWorldTranslation/english/2013-release",
        help="Base path for NWT Bible text files (default: %(default)s).",
    )
    nwt_parser.add_argument(
        "--output-file",
        type=str,
        default="data/nwt_bible.json",
        help="Output JSON file for NWT data (default: %(default)s).",
    )

    # Sub-command for loading KJ21/ASV to JSON
    kj21_parser = subparsers.add_parser(
        "load-kj21-asv",
        help="Load KJ21 and ASV Bible data from .txt files into JSON format.",
    )
    kj21_parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Input directory containing .txt files for KJ21/ASV.",
    )
    kj21_parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Output directory for generated JSON files.",
    )

    # Sub-command for extracting entities
    extract_parser = subparsers.add_parser(
        "extract-entities",
        help="Extract entities and occupations from Bible JSON data.",
    )
    extract_parser.add_argument(
        "--input-file",
        type=str,
        default="data/nwt_bible.json",
        help="Input JSON file for Bible data (default: %(default)s).",
    )
    extract_parser.add_argument(
        "--output-json",
        type=str,
        default="data/bible_entities.json",
        help="Output JSON file for extracted entities (default: %(default)s).",
    )
    extract_parser.add_argument(
        "--output-csv",
        type=str,
        default="data/bible_entities.csv",
        help="Output CSV file for extracted entities (default: %(default)s).",
    )
    extract_parser.add_argument(
        "--books",
        type=str,
        nargs="*",
        help="Specify one or more books to extract entities from (e.g., genesis exodus).",
    )
    extract_parser.add_argument(
        "--translation",
        type=str,
        default="nwt",
        help="Bible translation, ex: nwt | asv | kj21 ",
    )

    # Sub-command for searching Bible text
    search_parser = subparsers.add_parser(
        "search",
        help="Search for a phrase in the Bible text and display matches.",
    )
    search_parser.add_argument(
        "--input-file",
        type=str,
        default="data/nwt_bible.json",
        help="Input JSON file for Bible data (default: %(default)s).",
    )
    search_parser.add_argument(
        "--phrase",
        type=str,
        required=True,
        help="Phrase to search for in the Bible text.",
    )
    search_parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Number of top matches to display (default: %(default)s).",
    )
    search_parser.add_argument(
        "--csv",
        action="store_true",
        help="Output the results in CSV format.",
    )

    # Sub-command for extracting a specific reference
    reference_parser = subparsers.add_parser(
        "extract-reference",
        help="Extract text for a specific Bible reference.",
    )
    reference_parser.add_argument(
        "--input-file",
        type=str,
        default="data/nwt_bible.json",
        help="Input JSON file for Bible data (default: %(default)s).",
    )
    reference_parser.add_argument(
        "--reference",
        type=str,
        required=True,
        help="Bible reference to extract (e.g., 'Gen 1:1', 'John 3:16').",
    )
    reference_parser.add_argument(
        "--translation",
        type=str,
        required=True,
        help="Bible translation, ex: nwt | asv | kj21 ",
    )

    # Sub-command for extracting a specific translation
    translation_parser = subparsers.add_parser(
        "extract-translation",
        help="Extract a specific translation from the multi-translation JSON.",
    )
    translation_parser.add_argument(
        "--input-file",
        type=str,
        default="data/multi_translation.json",
        help="Input JSON file for multi-translation Bible data (default: %(default)s).",
    )
    translation_parser.add_argument(
        "--translation",
        type=str,
        required=True,
        help="Translation to extract (e.g., 'asv', 'kj21', 'nwt').",
    )
    translation_parser.add_argument(
        "--output-file",
        type=str,
        default="data/extracted_translation.json",
        help="Output JSON file for extracted translation (default: %(default)s).",
    )

    args = parser.parse_args()

    if args.command == "load-nwt":
        nwt_extractor.generate_bible_json(args.base_path, args.output_file)
    elif args.command == "load-kj21-asv":
        bible_extractor.extract_verses_from_txt(args.input_dir, args.output_dir)
    elif args.command == "extract-entities":
        entity_extractor.perform_entity_analysis(
            args.input_file,
            args.output_json,
            args.output_csv,
            args.translation,
            books=args.books,
        )
    elif args.command == "search":
        matches = search_engine.find_matches(
            args.input_file, args.phrase, top_n=args.top_n, output_csv=args.csv
        )
        if not args.csv:
            for match in matches:
                print(
                    f"{match['book']} {match['chapter']}:{match['verse']} - {match['text']}"
                )
    elif args.command == "extract-reference":
        result = entity_extractor.extract_reference(
            args.input_file, args.reference, args.translation
        )
        print(result)
    elif args.command == "extract-translation":
        with open(args.input_file, "r", encoding="utf-8") as f:
            multi_translation_data = json.load(f)

        single_translation_data = manipulator.extract_translation(
            multi_translation_data, args.translation
        )

        with open(args.output_file, "w", encoding="utf-8") as f:
            json.dump(single_translation_data, f, indent=4)

        print(f"Extracted {args.translation} translation saved to {args.output_file}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
