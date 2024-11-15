"""test main module"""

import unittest

import spacy

from main import extract_context  # Replace with your actual script name
from main import extract_entities_from_verse

# Load spaCy's English NLP model for testing
nlp = spacy.load("en_core_web_sm")


class TestMain(unittest.TestCase):
    """test main module"""

    def test_possessive_handling(self):
        """Test that possessive phrases are handled correctly."""
        text = "This is the history of Noah’s sons, Shem, Ham, and Japheth."
        doc = nlp(text)
        # Emulate entity recognition for "Shem"
        start, end = 5, 6  # Position of "Shem" in tokenized text
        context = extract_context(text, start, end)
        expected_context = "the history of Noah's sons, Shem, Ham"
        self.assertEqual(context, expected_context)

    def test_dangling_possessive(self):
        """Test that possessive phrases starting with a dangling "'s" are not misrepresented."""
        text = "His brother’s name was Jubal. He was the founder of all those who play the harp and the pipe."
        doc = nlp(text)
        # Emulate entity recognition for "Jubal"
        start, end = 4, 5  # Position of "Jubal" in tokenized text
        context = extract_context(text, start, end)
        expected_context = "His brother's name was Jubal. He"
        self.assertEqual(context, expected_context)

    def test_context_extraction(self):
        """Test general context extraction to ensure surrounding words are correctly captured."""
        text = "Adam's life was long and fulfilling, with many generations to come."
        doc = nlp(text)
        # Emulate entity recognition for "Adam"
        start, end = 0, 1  # Position of "Adam" in tokenized text
        context = extract_context(text, start, end)
        expected_context = "Adam's life was"
        self.assertEqual(context, expected_context)

    def test_entity_extraction_with_reference(self):
        """Test entity extraction function to ensure references are handled accurately."""
        verse_text = "This is the history of Noah’s sons, Shem, Ham, and Japheth."
        verse_num = 1
        entities = {"PERSON": {}}
        book = "01-Genesis"
        chapter = "010"
        extract_entities_from_verse(verse_text, verse_num, entities, book, chapter)

        # Expected output in entities dict
        expected_output = {
            "PERSON": {
                "Noah": {
                    "Count": 1,
                    "Context": [
                        {
                            "Reference": "Genesis 10:1",
                            "Text": "the history of Noah's sons",
                        }
                    ],
                },
                "Shem": {
                    "Count": 1,
                    "Context": [
                        {"Reference": "Genesis 10:1", "Text": "Noah's sons, Shem, Ham"}
                    ],
                },
            }
        }

        self.assertEqual(entities, expected_output)


if __name__ == "__main__":
    unittest.main()
