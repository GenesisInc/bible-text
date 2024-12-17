"""extractor"""

import json
import re
import sys

from bs4 import BeautifulSoup


def parse_txt_file(file_path, version, is_single_chapter_book=False):
    """Extract verses and text from a .txt file."""
    verses = {}
    current_chapter = None
    current_verse = None
    combined_text = ""

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for span in soup.select(".text"):
        chapternum = span.find("span", class_="chapternum")
        versenum = span.find("sup", class_="versenum")

        if chapternum:
            current_chapter = chapternum.get_text(strip=True).lstrip("0")
            current_verse = "1"  # Reset verse when chapter changes
            combined_text = ""

        if is_single_chapter_book:
            current_chapter = "1"

        if versenum:
            if combined_text and current_chapter and current_verse:
                verses.setdefault(current_chapter, {}).setdefault(current_verse, {})[
                    version
                ] = combined_text.strip()
            current_verse = versenum.get_text(strip=True).lstrip("0")
            combined_text = ""

        clean_text = clean_verse_text(span.get_text(strip=True), chapternum, versenum)
        combined_text += " " + clean_text

    if current_chapter and current_verse and combined_text:
        verses.setdefault(current_chapter, {}).setdefault(current_verse, {})[
            version
        ] = combined_text.strip()

    return verses


## cleanup versetext extracted from html fragment/bible-gateway
def clean_verse_text(raw_text, chapternum, versenum):
    """Clean raw text by removing chapter numbers, verse numbers, and footnotes."""
    if chapternum:
        raw_text = raw_text[len(chapternum.get_text(strip=True)) :]
    if versenum:
        raw_text = raw_text[len(versenum.get_text(strip=True)) :]
    raw_text = re.sub(r"\[[a-z]\]", "", raw_text)  # Remove footnotes
    return raw_text.strip()


# 1: "data/bibles/bible_gateway/NRSVCE/Exodus/9.fragment.html"
inp = sys.argv[1]
vers = sys.argv[2]
single_chapter = False
if len(sys.argv) > 3:
    single_chapter = sys.argv[3]
v = parse_txt_file(inp, vers, single_chapter)
print(json.dumps(v))
