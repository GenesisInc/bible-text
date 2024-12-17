import json
from bs4 import BeautifulSoup
from collections import OrderedDict


def extract_bible_book(filename):
    # Read the content of the file
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Ordered dictionary to hold the entire book
    book_data = OrderedDict()

    # Current chapter and its data
    current_chapter = None
    chapter_data = OrderedDict()

    # Extract text and group by chapters and verses
    for p in soup.find_all("p", class_="sb"):
        for span in p.find_all("span", class_="v"):
            # Detect chapter numbers (anchors with `cl vx vp` or `cl vp`)
            chapter_anchor = span.find("a", class_=["cl vx vp", "cl vp"])
            if chapter_anchor:
                # Extract chapter number
                chapter_number_tag = chapter_anchor.find("strong")
                if chapter_number_tag:
                    chapter_number = chapter_number_tag.get_text(strip=True)

                    # Save the previous chapter if any
                    if current_chapter:
                        book_data[current_chapter] = chapter_data

                    # Start a new chapter
                    current_chapter = chapter_number
                    chapter_data = OrderedDict()

                    # Process the first verse (from the same span)
                    verse_text = "".join(span.stripped_strings)
                    clean_verse_text = verse_text[len(current_chapter) :].strip()
                    chapter_data["1"] = {"study bible": clean_verse_text}
                    continue  # Continue to process other spans in the same paragraph

            # Extract verse number and text (for non-chapter spans)
            verse_anchor = span.find("a", class_="vl vx vp")
            if verse_anchor:
                verse_number = verse_anchor.get_text(strip=True)
                verse_text = "".join(span.stripped_strings)

                # Clean up verse text by removing the duplicate verse number
                clean_verse_text = verse_text[len(verse_number) :].strip()
                chapter_data[verse_number] = {"study bible": clean_verse_text}

    # Save the last chapter (if not already saved)
    if current_chapter and current_chapter not in book_data:
        book_data[current_chapter] = chapter_data

    # Return ordered book data
    return book_data


if __name__ == "__main__":
    # Sequentially iterate through books 1 to 66
    base_path = "data/bibles/bible_gateway/jw_study/"
    bible_books = OrderedDict()

    for book_number in range(1, 67):
        try:
            # Construct the filename
            filename = f"{base_path}{book_number}.html"

            # Extract the book data
            bible_books[str(book_number)] = extract_bible_book(filename)
            print(f"Processed book: {book_number}")
        except FileNotFoundError:
            print(f"File not found for book {book_number}. Skipping...")
        except Exception as e:
            print(f"Error processing book {book_number}: {e}")

    # Write all books to a single JSON file
    with open("bible_books.json", "w", encoding="utf-8") as file:
        json.dump(bible_books, file, indent=2, ensure_ascii=False)

    print("Bible books saved to bible_books.json")
