import json


def save_to_json(data, output_file):
    """Save data to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_from_json(input_file):
    """Load data from a JSON file."""
    with open(input_file, "r", encoding="utf-8") as f:
        return json.load(f)
