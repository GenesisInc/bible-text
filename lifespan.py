import spacy
import re
import json


# Load spaCy's English NLP model
nlp = spacy.load("en_core_web_sm")

# Lifespan indicators and exclusions
LIFESPAN_INDICATORS = {"lived for", "was", "amounted to", "were", "to be"}
EXCLUSION_KEYWORDS = {"reigned", "gathered to", "length of", "satisfied with years"}


def extract_numeric_value(verse_text):
    """Extracts a numeric value from verse_text if it’s purely numeric."""
    numeric_text = re.sub(r"[^\d]", "", verse_text)
    return int(numeric_text) if numeric_text.isdigit() else None


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


def get_reference(book, chapter, verse_number):
    """Generates a reference string in 'Book Chapter:Verse' format."""
    return f"{book} {chapter}:{verse_number}"


def add_lifespan_entry(
    lifespans_dict, person, years, confidence, reference, context_text
):
    """Adds a lifespan entry to the lifespans dictionary."""
    if person not in lifespans_dict:
        lifespans_dict[person] = []
    lifespans_dict[person].append(
        {
            "Explicit Lifespan": years,
            "Confidence": round(confidence, 2),
            "Context": {"Reference": reference, "Text": context_text},
        }
    )


def detect_lifespan_phrases(verse_text, book="Genesis", chapter="16"):
    """Detects phrases indicating a person's lifespan with verse
    references and confidence scores."""
    doc = nlp(verse_text)
    lifespans_dict = {}

    for verse_number, sent in enumerate(doc.sents, start=1):
        person, years = None, None
        reference = get_reference(book, chapter, verse_number)

        for ent in sent.ents:
            if ent.label_ == "PERSON":
                person = ent.text
            elif ent.label_ in {"CARDINAL", "DATE"}:
                years = extract_numeric_value(ent.text)
                if years is not None:
                    confidence = calculate_confidence(sent.text.lower())
                    if confidence > 0 and person:
                        add_lifespan_entry(
                            lifespans_dict,
                            person,
                            years,
                            confidence,
                            reference,
                            sent.text.strip(),
                        )

    return lifespans_dict


# Sample text containing different lifespan statements
text = """
Adam lived for 130 years and then became father to a son in his likeness, in his image, and he named him Seth.
After becoming father to Seth, Adam lived for 800 years. And he became father to sons and daughters.
So all the days of Adam’s life amounted to 930 years, and then he died.
Noah lived for 950 years, and then he died.
The days of Terah were 205 years. Then Terah died in Haran.
And Sarah lived for 127 years; these were the years of Sarah’s life. So Sarah died in Kir'i·ath-ar'ba.
7 The years of Abraham’s life were 175 years. 8 Then Abraham breathed his last and died at a good old age, old and satisfied, and was gathered to his people.
17 And Ishʹma·el lived for 137 years. Then he breathed his last and died and was gathered to his people.
28 Isaac lived to be 180 years old. 29 Then Isaac breathed his last and died and was gathered to his people, after a long and...
26 And Joseph died at the age of 110, and they had him embalmed, and he was put in a coffin in Egypt.
39 Aaron was 123 years old at his death on Mount Hor.
7 Moses was 120 years old at his death.
15 When Je·hoiʹa·da was old and satisfied with years, he died; he was 130 years old at his death.
3 Adam lived for 130 years and then became father to a son in his likeness, in his image, and he named him Seth. 4 After becoming father to Seth, Adam lived for 800 years. And he became father to sons and daughters. 5 So all the days of Adam’s life amounted to 930 years, and then he died.
6 Seth lived for 105 years and then became father to Eʹnosh. 7 After becoming father to Eʹnosh, Seth lived for 807 years. And he became father to sons and daughters. 8 So all the days of Seth amounted to 912 years, and then he died.
9 Eʹnosh lived for 90 years and then became father to Keʹnan. 10 After becoming father to Keʹnan, Eʹnosh lived for 815 years. And he became father to sons and daughters. 11 So all the days of Eʹnosh amounted to 905 years, and then he died.
12 Keʹnan lived for 70 years and then became father to Ma·halʹa·lel. 13 After becoming father to Ma·halʹa·lel, Keʹnan lived for 840 years. And he became father to sons and daughters. 14 So all the days of Keʹnan amounted to 910 years, and then he died.
15 Ma·halʹa·lel lived for 65 years and then became father to Jaʹred. 16 After becoming father to Jaʹred, Ma·halʹa·lel lived for 830 years. And he became father to sons and daughters. 17 So all the days of Ma·halʹa·lel amounted to 895 years, and then he died.
18 Jaʹred lived for 162 years and then became father to Eʹnoch. 19 After becoming father to Eʹnoch, Jaʹred lived for 800 years. And he became father to sons and daughters. 20 So all the days of Jaʹred amounted to 962 years, and then he died.
21 Eʹnoch lived for 65 years and then became father to Me·thuʹse·lah. 22 After becoming father to Me·thuʹse·lah, Eʹnoch continued to walk with the true God for 300 years. And he became father to sons and daughters. 23 So all the days of Eʹnoch amounted to 365 years. 24 Eʹnoch kept walking with the true God. Then he was no more, for God took him.
25 Me·thuʹse·lah lived for 187 years and then became father to Laʹmech. 26 After becoming father to Laʹmech, Me·thuʹse·lah lived for 782 years. And he became father to sons and daughters. 27 So all the days of Me·thuʹse·lah amounted to 969 years, and then he died.
28 Laʹmech lived for 182 years and then became father to a son. 29 He named him Noah, saying: “This one will bring us comfort from our labor and from the painful toil of our hands because of the ground that Jehovah has cursed.” 30 After becoming father to Noah, Laʹmech lived for 595 years. And he became father to sons and daughters. 31 So all the days of Laʹmech amounted to 777 years, and then he died.
28 Noah continued to live for 350 years after the Flood. 29 So all the days of Noah amounted to 950 years, and he died.
32 The days of Teʹrah were 205 years. Then Teʹrah died in Haʹran.
1 And Sarah lived for 127 years; these were the years of Sarah’s life. 2 So Sarah died in Kirʹi·ath-arʹba,
28 Isaac lived to be 180 years old. 29 Then Isaac breathed his last and died and was gathered to his people
22 And Joseph continued to dwell in Egypt, he and the household of his father, and Joseph lived for 110 years.
The same man hurried in and reported the news to Eʹli. 15 (Now Eʹli was 98 years old, and his eyes stared straight ahead, and he could not see.)
26 Thus David the son of Jesʹse reigned over all Israel, 27 and the length of his reign over Israel was 40 years. In Hebʹron he reigned for 7 years, and in Jerusalem he reigned for 33 years. 28 And he died at a good old age, satisfied with long life, wealth, and glory; and his son Solʹo·mon became king in his place.
20 He was 32 years old when he became king, and he reigned for eight years in Jerusalem. No one regretted it when he died.
15 When Je·hoiʹa·da was old and satisfied with years, he died; he was 130 years old at his death.
16 After this Job lived for 140 years, and he saw his children and his grandchildren—four generations. 17 Finally Job died, after a long and satisfying life.
"""

# Run the detection function
lifespans = detect_lifespan_phrases(text)

# Print the output in JSON format
print(json.dumps(lifespans, indent=2))
