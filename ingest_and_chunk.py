import json
import re
from pathlib import Path
import random

import requests
from bs4 import BeautifulSoup

try:
    import tiktoken
    tokenizer = tiktoken.get_encoding("cl100k_base")
except ImportError:
    tokenizer = None


SOURCES = [
    {
        "source": "PlanetTerp CMSC132 Reviews",
        "url": "https://planetterp.com/course/CMSC132/reviews",
        "type": "reviews",
    },
    {
        "source": "PlanetTerp CMSC216 Reviews",
        "url": "https://planetterp.com/course/CMSC216/reviews",
        "type": "reviews",
    },
    {
        "source": "PlanetTerp CMSC250",
        "url": "https://planetterp.com/course/CMSC250",
        "type": "reviews",
    },
    {
        "source": "PlanetTerp CMSC330 Reviews",
        "url": "https://planetterp.com/course/CMSC330/reviews",
        "type": "reviews",
    },
    {
        "source": "PlanetTerp CMSC351",
        "url": "https://planetterp.com/course/CMSC351",
        "type": "reviews",
    },
    {
        "source": "PlanetTerp Justin Wyss-Gallifent",
        "url": "https://planetterp.com/professor/wyss-gallifent",
        "type": "reviews",
    },
    {
        "source": "PlanetTerp Larry Herman",
        "url": "https://planetterp.com/professor/herman_larry",
        "type": "reviews",
    },
    {
        "source": "Rate My Professors Fawzi Emad",
        "url": "https://www.ratemyprofessors.com/professor/313062",
        "type": "reviews",
    },
    {
        "source": "Rate My Professors Ilchul Yoon",
        "url": "https://www.ratemyprofessors.com/professor/2327417",
        "type": "reviews",
    },
    {
        "source": "Christopher Kauffman CMSC216 Course Page",
        "url": "https://www.cs.umd.edu/~profk/216/",
        "type": "long_page",
    },
]


RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")
OUTPUT_FILE = Path("data/chunks.json")

RAW_DIR.mkdir(parents=True, exist_ok=True)
CLEAN_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


def safe_filename(name):
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", name).strip("_").lower()


def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return response.text


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")
    text = text.replace("&#39;", "'")
    return text.strip()


def remove_boilerplate(soup):
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "button"]):
        tag.decompose()

    return soup


def html_to_clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    soup = remove_boilerplate(soup)

    text = soup.get_text(separator="\n")
    lines = []

    bad_phrases = [
        "sign in",
        "log in",
        "create account",
        "cookie",
        "privacy policy",
        "terms of service",
        "advertisement",
        "share",
        "read more",
    ]

    for line in text.splitlines():
        line = clean_text(line)

        if not line:
            continue

        if any(phrase in line.lower() for phrase in bad_phrases):
            continue

        lines.append(line)

    return "\n".join(lines)


def count_tokens(text):
    if tokenizer:
        return len(tokenizer.encode(text))

    return len(text.split())


def token_chunks(text, chunk_size=900, overlap=125):
    if tokenizer:
        tokens = tokenizer.encode(text)
        chunks = []

        start = 0
        while start < len(tokens):
            end = start + chunk_size
            chunk = tokenizer.decode(tokens[start:end])
            chunks.append(chunk.strip())
            start += chunk_size - overlap

        return chunks

    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk.strip())
        start += chunk_size - overlap

    return chunks


def extract_review_chunks(html, source_name, url):
    soup = BeautifulSoup(html, "html.parser")
    soup = remove_boilerplate(soup)

    candidates = []

    selectors = [
        "[class*=review]",
        "[class*=Review]",
        "article",
        ".card",
    ]

    for selector in selectors:
        for block in soup.select(selector):
            text = clean_text(block.get_text(separator=" "))
            if 40 <= len(text) <= 3000:
                candidates.append(text)

    unique_reviews = []
    seen = set()

    for text in candidates:
        normalized = text.lower()

        if normalized in seen:
            continue

        bad_review_phrases = [
            "Professor TA Expected Grade",
            "Expected Grade A+",
            "Add a new Professor",
            "Review submitted successfully",
            "Not sure what to write",
            "Professor Filter",
            "Sort By",
            "Register to save your reviews",
        ]

        if len(text.split()) < 12:
            continue

        if any(phrase.lower() in text.lower() for phrase in bad_review_phrases):
            continue

        seen.add(normalized)
        unique_reviews.append(text)

    chunks = []

    if unique_reviews:
        for i, review in enumerate(unique_reviews):
            chunks.append({
                "chunk_id": f"{safe_filename(source_name)}_review_{i}",
                "source": source_name,
                "url": url,
                "chunk_type": "single_review",
                "text": review,
                "token_count": count_tokens(review),
            })

    return chunks


def make_chunks(source, cleaned_text, html):
    source_name = source["source"]
    url = source["url"]
    source_type = source["type"]

    chunks = []

    if source_type == "reviews":
        chunks = extract_review_chunks(html, source_name, url)

        if chunks:
            return chunks

    longer_chunks = token_chunks(
        cleaned_text,
        chunk_size=900,
        overlap=125
    )

    for i, chunk in enumerate(longer_chunks):
        chunks.append({
            "chunk_id": f"{safe_filename(source_name)}_chunk_{i}",
            "source": source_name,
            "url": url,
            "chunk_type": "token_chunk",
            "text": chunk,
            "token_count": count_tokens(chunk),
        })

    return chunks


def main():
    all_chunks = []

    for source in SOURCES:
        source_name = source["source"]
        url = source["url"]
        filename = safe_filename(source_name)

        print(f"Loading: {source_name}")

        try:
            html = fetch_html(url)

            raw_path = RAW_DIR / f"{filename}.html"
            raw_path.write_text(html, encoding="utf-8")

            cleaned_text = html_to_clean_text(html)

            clean_path = CLEAN_DIR / f"{filename}.txt"
            clean_path.write_text(cleaned_text, encoding="utf-8")

            if source_name == "PlanetTerp CMSC132 Reviews":
                print("\nPreview of one cleaned document:")
                print("=" * 80)
                print(cleaned_text[:3000])
                print("=" * 80)
            chunks = make_chunks(source, cleaned_text, html)
            all_chunks.extend(chunks)

            print(f"Created {len(chunks)} chunks")

        except Exception as error:
            print(f"Failed to load {url}")
            print(error)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print("\nDone.")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Saved chunks to: {OUTPUT_FILE}")

    print("\nFive sample chunks:\n")

    for chunk in random.sample(all_chunks, min(5, len(all_chunks))):
        print("=" * 80)
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Source: {chunk['source']}")
        print(f"URL: {chunk['url']}")
        print(f"Type: {chunk['chunk_type']}")
        print(f"Token count: {chunk['token_count']}")
        print("-" * 80)
        print(chunk["text"][:1200])
        print()


if __name__ == "__main__":
    main()