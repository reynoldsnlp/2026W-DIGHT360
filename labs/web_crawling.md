# Web Crawling Lab

## 0. Allowed Imports

Use only standard library tools (`pathlib`, `time`, `urllib`) plus the packages installed for this lab (`justhtml`, `requests`).

## 1. Create a `scrape` Directory

Use this code at the top of your module to create a `scrape/` directory if it doesn't already exist:

```python
from pathlib import Path

Path("scrape").mkdir(exist_ok=True)
```

## 2. Write `get_reynoldsnlp(filename)`

Create a function named `get_reynoldsnlp` that takes one argument, `filename`.

- Request `filename` from `http://reynoldsnlp.com/scrape/`.
- Save the downloaded HTML file into the local `scrape/` folder.
- Include a `1`-second pause between requests inside this function (use `time.sleep()`).
- The function should not return a value.

Example:

- Input: `'aa.html'`
- Request: `http://reynoldsnlp.com/scrape/aa.html`
- Save to: `scrape/aa.html`

## 3. Write `parse_hrefs(filename)`

Create a function named `parse_hrefs` that takes one argument, `filename`.

- Open the local file from `scrape/`.
- Parse the HTML using `justhtml` (not BeautifulSoup).
- Extract all `<a>` tag `href` values.
- Keep only links that contain `reynoldsnlp.com/scrape`.
- Return filenames only (for example, `ab.html`, not the full URL).
- Ignore links outside `/scrape/` (including `crawl_trap.html`).

Important:

- If your results include `crawl_trap.html`, your filtering is incorrect.

Minimal parsing sketch (API names may vary by version; use the equivalent from `justhtml`):

```python
from pathlib import Path
from urllib.parse import urlparse
import justhtml

html = Path("scrape") / filename
doc = justhtml.parse(html.read_text(encoding="utf-8", errors="ignore"))

filenames = []
for link in doc.select("a"):
    href = link.attributes.get("href")
    if not href:
        continue
    if "reynoldsnlp.com/scrape/" not in href:
        continue
    filenames.append(Path(urlparse(href).path).name)
```

Example:

- If links include:
  - `http://reynoldsnlp.com/scrape/ab.html`
  - `http://reynoldsnlp.com/scrape/ac.html`
  - `http://reynoldsnlp.com/crawl_trap.html`
- Then `parse_hrefs("aa.html")` should return:
  - `['ab.html', 'ac.html']`

## 4. Crawl With Sets

Use the two functions above to build a crawler.

- Create a to-do set with one seed filename: `{'aa.html'}`.
- Create an empty `visited` set for already-requested filenames.
- Loop until the to-do set is empty:
  - Pop one filename from the to-do set.
  - If it is already in `visited`, skip it.
  - Request and save the page.
  - Add that filename to `visited`.
  - Parse and extract matching hrefs.
  - Add only unseen filenames to the to-do set.

Clean set pattern:

```python
todo.update(new_filenames - visited)
```

## 5. Expected Result

When complete, you should have **80 files** in the `scrape/` directory.

- The site contains many duplicate links.
- Your script must request each filename at most once.
- Your crawler should not enter an infinite loop.

## 6. Style and Ethics Requirements

- Follow ethical scraping practices.
- Include a `1`- or `2`-second pause between requests.
- Follow PEP 8 and keep your code readable.

## 7. Submission Checklist

- `scrape/` is created automatically.
- `get_reynoldsnlp(filename)` uses `requests` to download pages, saves them locally, and returns `None`.
- `parse_hrefs(filename)` uses `justhtml` and returns filenames only.
- Crawler uses sets for `todo` and `visited`.
- Crawler does not revisit pages and does not hit `crawl_trap.html`.
- Exactly `80` files are saved in `scrape/`.
- Final reflection comments are included.

## 8. Add Two Final Comments to Your Module

On the last lines of your module, add comments answering:

1. What filename pattern do you see in the saved files, and which filename is missing from the pattern?
2. Why are sets better than lists for tracking both to-do and already-requested filenames?
