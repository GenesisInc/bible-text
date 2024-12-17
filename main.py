"""main"""

import argparse
import json
import os

from extraction import bible_extractor, manipulator, nwt_extractor


def setup_parsers():
    """Set up argument parsers for all sub-commands."""
    parser = argparse.ArgumentParser(
        description="CLI to process Bible text, extract entities, and perform searches."
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    setup_load_nwt_parser(subparsers)
    setup_load_gateway_parser(subparsers)
    setup_merge_translation_parser(subparsers)

    return parser


def setup_load_nwt_parser(subparsers):
    """setup load-jworg parser"""
    nwt_parser = subparsers.add_parser(
        "load-jworg",
        help="Load New World Translation (NWT) data into JSON format.",
    )
    nwt_parser.add_argument(
        "--input-dir",
        type=str,
        default="newWorldTranslation/english/2013-release",
        help="Base path for NWT Bible text files (default: %(default)s).",
    )
    nwt_parser.add_argument(
        "--output-dir",
        type=str,
        default="data/nwt_bible.json",
        help="Output dir (default: %(default)s).",
    )


def setup_load_gateway_parser(subparsers):
    """setup load-gateway parser"""
    gateway_parser = subparsers.add_parser(
        "load-gateway",
        help="Load bible-gateway translations from .txt files into JSON format.",
    )
    gateway_parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Input directory containing .txt files for KJ21/ASV.",
    )
    gateway_parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Output directory for generated JSON files.",
    )


def setup_merge_translation_parser(subparsers):
    """setup merge-translation parser"""
    merge_parser = subparsers.add_parser(
        "merge-translation",
        help="merge a specific translation to multi-translation JSON.",
    )
    merge_parser.add_argument(
        "--input-file",
        type=str,
        default="data/nwt_bible.json",
        help="Input JSON file to merge to multi-translation.json (default: %(default)s).",
    )
    merge_parser.add_argument(
        "--translation",
        type=str,
        required=True,
        help="Translation to extract (e.g., 'asv', 'kj21', 'nwt').",
    )
    merge_parser.add_argument(
        "--output-file",
        type=str,
        default="data/extracted_translation.json",
        help="Output JSON file for extracted translation (default: %(default)s).",
    )


def handle_command(args):
    """Handle the parsed command."""
    if args.command == "load-jworg":
        nwt_extractor.generate_bible_json(
            args.input_dir, os.path.join(args.output_dir, "nwt_bible.json")
        )
    elif args.command == "load-gateway":
        bible_extractor.extract_verses_from_txt(args.input_dir, args.output_dir)
    elif args.command == "merge-translation":
        with open(args.output_file, "r", encoding="utf-8") as out:
            multi_translation_data = json.load(out)
        with open(args.input_file, "r", encoding="utf-8") as inp:
            input_translation_data = json.load(inp)

        merged_data = manipulator.merge_translations(
            input_translation_data, multi_translation_data, args.translation
        )
        with open(args.output_file, "w", encoding="utf-8") as f:
            json.dump(merged_data, f, indent=4)

        print(f"Merged {args.translation} translation saved to {args.output_file}")
    else:
        print("Invalid command. Use --help for available options.")


def main():
    """Main function to handle CLI."""
    parser = setup_parsers()
    args = parser.parse_args()
    handle_command(args)


if __name__ == "__main__":
    main()
