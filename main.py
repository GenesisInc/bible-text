# bible-text/main.py
"""main module."""

import argparse
import json

# from extraction import bible_extractor, manipulator, nwt_extractor
from core.translation_loader import (
    bible_gw_loader,
    jw_loader,
    nwt_study,
    translation_manager,
)


def setup_parsers():
    """Set up argument parsers for all sub-commands."""
    parser = argparse.ArgumentParser(
        description="CLI to process Bible text, extract entities, and perform searches."
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    setup_load_nwt_parser(subparsers)
    setup_load_nwt_study_parser(subparsers)
    setup_load_gateway_parser(subparsers)
    setup_merge_translation_parser(subparsers)

    return parser


def setup_load_nwt_parser(subparsers):
    """Prepare load-jworg parser."""
    nwt_parser = subparsers.add_parser(
        "load-jworg",
        help="Load New World Translation (NWT) data into JSON format.",
    )
    nwt_parser.add_argument(
        "--input-dir",
        type=str,
        default="data/bibles/jw_org/nwt",
        help="Base path for NWT Bible text files (default: %(default)s).",
    )
    nwt_parser.add_argument(
        "--output-dir",
        "--output-dir",
        type=str,
        default="data/tmp",
        help="Output dir (default: %(default)s).",
    )


def setup_load_nwt_study_parser(subparsers):
    """Prepare load-jworg parser."""
    nwt_parser = subparsers.add_parser(
        "load-nwt-study",
        help="Load New World Translation (NWT) study bible data into JSON format.",
    )
    nwt_parser.add_argument(
        "--input-dir",
        type=str,
        default="data/bibles/jw_org/study",
        help="Base path for NWT Bible text files (default: %(default)s).",
    )
    nwt_parser.add_argument(
        "--output-dir",
        type=str,
        default="data/tmp",
        help="Output dir (default: %(default)s).",
    )
    nwt_parser.add_argument(
        "--translation",
        type=str,
        default="nwt-study",
        help="Output dir (default: %(default)s",
    )
    nwt_parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate generated JSON files (default: False).",
    )


def setup_load_gateway_parser(subparsers):
    """Prepare load-gateway parser."""
    gateway_parser = subparsers.add_parser(
        "load-gateway",
        help="Load bible-gateway translations from .txt files into JSON format.",
    )
    gateway_parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Input directory containing .txt files for KJ21/ASV.",
        default="data/bibles/bible_gateway",
    )
    gateway_parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        default="data/tmp",
        help="Output directory for generated JSON files.",
    )


def setup_merge_translation_parser(subparsers):
    """Prepare merge-translation parser."""
    merge_parser = subparsers.add_parser(
        "merge-translation",
        help="merge a specific translation to multi-translation JSON.",
    )
    merge_parser.add_argument(
        "--input-file",
        type=str,
        default="data/nwt_bible.json",
        help="Input JSON file to merge to multi-translation.json (default: %(default)s).",  # noqa: E501
    )
    merge_parser.add_argument(
        "--translation",
        type=str,
        required=True,
        default="nwt",
        help="Translation to extract (e.g., 'asv', 'kj21', 'nwt').",
    )
    merge_parser.add_argument(
        "--output-file",
        type=str,
        default="data/tmp/multi_translation.json",
        help="merged JSON file (default: %(default)s).",
    )


def handle_command(args):
    """Handle the parsed command."""
    if args.command == "load-jworg":
        jw_loader.generate_bible_json(
            args.input_dir,
            args.output_dir,
            "nwt",
        )
    elif args.command == "load-nwt-study":
        nwt_study.convert_all_books(
            args.input_dir,
            args.output_dir,
            args.translation,
        )
        if args.validate:
            nwt_study.validate_json_files(args.output_dir, args.translation)

    elif args.command == "load-gateway":
        bible_gw_loader.extract_verses_from_txt(args.input_dir, args.output_dir)
    elif args.command == "merge-translation":
        with open(args.output_file, encoding="utf-8") as out:
            multi_translation_data = json.load(out)
        with open(args.input_file, encoding="utf-8") as inp:
            input_translation_data = json.load(inp)

        merged_data = translation_manager.merge_translations(
            input_translation_data, multi_translation_data, args.translation
        )
        with open(args.output_file, "w", encoding="utf-8") as f:
            json.dump(merged_data, f, indent=4)

        print(f"Merged {args.translation} translation saved to {args.output_file}")
    else:
        print("Invalid command. Use --help for available options.")


def main():
    """Drives CLI application."""
    parser = setup_parsers()
    args = parser.parse_args()
    handle_command(args)


if __name__ == "__main__":
    main()
