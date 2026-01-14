"""DIGHT360 — Unit 01 Lab: Python Basics for Text Processing

Directions
- Work top-to-bottom.
- Each part provides any needed data.
- Replace each `...` with working Python code.
- Prefer small, clear steps; use the stdlib only.

This lab focuses on:
- Importing from the Python standard library
- Unpacking tuples/lists into multiple variables
- Writing functions
- Reading/writing files (including legacy encodings)
- Regular expressions for finding data in text
- Sorting with a lambda (e.g., by last letter)

"""

from pathlib import Path

LAB_DIR = Path(__file__).parent
ENCODINGS_DIR = LAB_DIR / "encodings"
OUTPUT_DIR = LAB_DIR / "unit01_output"


# -----------------------------
# Part 1 — Importing from stdlib
# -----------------------------

"""Task

1) Import these from the standard library:
   - `re`
   - `Counter` from `collections`
   - `statistics` (module)

2) Using ONLY those imports (plus built-ins), compute:
   - the mean and median of the numbers in this list
   - a frequency table of the letters in `"banana"`

Replace each `...` below.
"""

NUMBERS = [10, 20, 20, 30, 100]

# TODO: imports
...

# TODO: mean + median
mean_value = ...
median_value = ...

# TODO: Counter of letters
banana_counts = ...


# -----------------------------
# Part 2 — Unpacking tuples/lists
# -----------------------------

"""Task

1) Unpack the first tuple in SAMPLE_TUPLES into (label, count).
2) Unpack the list `triple = ["x", "y", "z"]` into three variables.
3) Unpack the first and last items of WORD_LIST into two variables, using `*rest`.

Replace each `...` below.
"""

SAMPLE_TUPLES: list[tuple[str, int]] = [
    ("alpha", 3),
    ("beta", 1),
    ("gamma", 2),
]

WORD_LIST: list[str] = [
    "token",
    "lemma",
    "corpus",
    "python",
    "regex",
    "unicode",
    "byte",
    "string",
]

first_tuple = SAMPLE_TUPLES[0]
label, count = ...

triple = ["x", "y", "z"]
a, b, c = ...

first_word, *middle_words, last_word = ...


# -----------------------------
# Part 3 — Writing small functions
# -----------------------------

"""Task

Write the functions below.

- `normalize_whitespace(text)`:
   * converts all whitespace runs (spaces/tabs/newlines) into a single space
   * strips leading/trailing whitespace

- `tokenize_simple(text)`:
   * lowercases text
   * returns a list of word tokens consisting of letters only (A-Z)
   * no punctuation, no digits

Hint: You may use `re`.
"""


def normalize_whitespace(text: str) -> str:
    ...


def tokenize_simple(text: str) -> list[str]:
    ...


# -----------------------------
# Part 4 — Regex: finding data in text
# -----------------------------

"""Task

Use `re` to extract information from RAW_TEXT.

Implement:
- `find_emails(text)` returning a list of email strings
- `find_phone_numbers(text)` returning a list of phone number strings
- `find_hashtags(text)` returning a list like ["TextProcessing", "DIGHT360"]

Keep patterns simple and readable; do not aim for RFC-perfect email matching.
"""

RAW_TEXT = (
    "Contact: Ada Lovelace <ada@analytical.engine>\n"
    "Backup: team+nlp@school.edu\n"
    "Office: (555) 123-4567\n"
    "Alt: 555-000-9999\n"
    "Dates: 2026-01-12, 01/13/2026, and Jan 14, 2026\n"
    "Hashtags: #TextProcessing #DIGHT360\n"
)


def find_emails(text: str) -> list[str]:
    ...


def find_phone_numbers(text: str) -> list[str]:
    ...


def find_hashtags(text: str) -> list[str]:
    ...


# -----------------------------
# Part 5 — Reading files with encodings
# -----------------------------

"""Task

You are provided two files in labs/encodings/:
- latin1_poem.txt  (ISO-8859-1 / latin-1)
- cp1252_quotes.txt (Windows-1252)

1) Read each file using the correct encoding.
2) Combine them into one UTF-8 file named `combined_utf8.txt` in OUTPUT_DIR.
3) In the combined output, ensure every line ends with a single '\n'.

Replace each `...` below.
"""

LATIN1_PATH = ENCODINGS_DIR / "latin1_poem.txt"
CP1252_PATH = ENCODINGS_DIR / "cp1252_quotes.txt"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
COMBINED_PATH = OUTPUT_DIR / "combined_utf8.txt"

# TODO: read with correct encodings
latin1_text = ...
cp1252_text = ...

# TODO: write combined output as UTF-8
...


# -----------------------------
# Part 6 — Writing files + round-trip check
# -----------------------------

"""Task

1) Write a small TSV file `word_counts.tsv` (UTF-8) into OUTPUT_DIR.
2) The file should contain two columns: word<TAB>count.
3) Use the tokens from tokenize_simple() over COMBINED_PATH's contents.
4) Sort rows by descending count, then ascending word.

Replace each `...` below.
"""

WORD_COUNTS_PATH = OUTPUT_DIR / "word_counts.tsv"

# TODO: read combined UTF-8
combined_text = ...

# TODO: tokenize and count
tokens = ...
counts = ...

# TODO: sort rows
rows = ...

# TODO: write TSV
...


# -----------------------------
# Part 7 — Lambda sort by last letter
# -----------------------------

"""Task

Sort WORD_LIST by:
1) the last letter of each word
2) then by the whole word (to break ties)

Use `sorted(..., key=...)` with a lambda.
Replace each `...` below.
"""

WORD_LIST: list[str] = [
    "token",
    "lemma",
    "corpus",
    "python",
    "regex",
    "unicode",
    "byte",
    "string",
]

sorted_by_last_letter = ...


# -----------------------------
# Optional: self-check (run this file)
# -----------------------------

"""These checks are intentionally mild.

Once you've replaced all `...`, running `python3 labs/unit01.py` should:
- create files in labs/unit01_output/
- print a short report
"""


def main() -> None:
    # Part 1 checks
    print("Part 1:")
    print("  mean:", mean_value)
    print("  median:", median_value)
    print("  banana counts:", dict(banana_counts))

    # Part 2 checks
    print("Part 2:")
    print("  unpacked tuple:", label, count)
    print("  triple:", a, b, c)
    print("  first/last:", first_word, last_word)

    # Part 4 checks
    print("Part 4:")
    print("  emails:", find_emails(RAW_TEXT))
    print("  phones:", find_phone_numbers(RAW_TEXT))
    print("  hashtags:", find_hashtags(RAW_TEXT))

    # Part 5/6 checks
    print("Part 5/6:")
    print("  wrote:", COMBINED_PATH)
    print("  wrote:", WORD_COUNTS_PATH)

    # Part 7 check
    print("Part 7:")
    print("  sorted by last letter:", sorted_by_last_letter)


if __name__ == "__main__":
    main()
