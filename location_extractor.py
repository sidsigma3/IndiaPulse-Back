import spacy

nlp = spacy.load("en_core_web_sm")

def extract_locations(text: str) -> list[str]:
    """
    Extract city/state names from news text
    """
    if not text:
        return []

    doc = nlp(text)
    locations = set()

    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            locations.add(ent.text)

            

    return list(locations)
