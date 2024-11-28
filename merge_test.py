"""test_merge_single_translation_to_multi"""

import json

from extraction.manipulator import merge_translations
from utils import file_utils


def test_merge_single_translation_to_multi():
    """test_merge_single_translation_to_multi"""
    multi_translation_path = "data/multi_translation.json"
    single_translation_path = "data/nwt_bible.json"
    output_path = "data/merged_translation.json"

    # Load multi-translation JSON
    with open(multi_translation_path, "r", encoding="utf-8") as f:
        multi_translation_data = json.load(f)

    # Load single-translation JSON (e.g., NWT)
    with open(single_translation_path, "r", encoding="utf-8") as f:
        single_translation_data = json.load(f)

    # Merge the single translation into the multi-translation structure
    merged_translation = merge_translations(
        single_translation_data, multi_translation_data, "nwt"
    )

    # Save the result
    file_utils.save_to_json(merged_translation, output_path)

    print(f"Merged translation saved to {output_path}")


if __name__ == "__main__":
    test_merge_single_translation_to_multi()
