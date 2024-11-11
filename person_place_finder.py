import spacy

# Load spaCy's English NLP model
nlp = spacy.load("en_core_web_sm")

# Paths to input and output files
input_file = "tmp/names.list"  # Adjust path as needed
person_output_file = "tmp/person-names.list"
place_output_file = "tmp/place-names.list"

# Initialize sets to store unique names and places
person_names = set()
place_names = set()

# Read the input file and process each word
with open(input_file, "r") as file:
    for line in file:
        count, word = line.strip().split(maxsplit=1)

        # Use spaCy to process the word and identify entities
        doc = nlp(word)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                person_names.add(word)
            elif ent.label_ == "GPE":  # GPE (Geopolitical Entity) for places
                place_names.add(word)

# Write results to separate files
with open(person_output_file, "w") as person_file:
    for name in sorted(person_names):
        person_file.write(f"{name}\n")

with open(place_output_file, "w") as place_file:
    for place in sorted(place_names):
        place_file.write(f"{place}\n")

print("Extraction complete! Check 'person-names.list' and 'place-names.list' for results.")