# Scripture Similarity Search

In this lab you will use [Sentence Transformers](https://sbert.net/) to find
scriptures in the Book of Mormon that are *semantically* similar to a given
verse — without writing any hand-crafted linguistic features.

The work is split into two scripts:

| Script | Purpose |
|---|---|
| `scripture_preprocess.py` | Download/load data, encode every verse, save embeddings to disk |
| `scripture_search.py` | Prompt the user for a reference and return the top 10 similar verses |

---

## Background

A **Sentence Transformer** model converts a piece of text into a dense
numerical vector (an *embedding*) such that texts with similar meanings end up
close together in vector space.  Cosine similarity between two such vectors
gives a score between −1 and 1 — the higher the score, the more semantically
similar the texts.

Because encoding thousands of verses is slow, you will encode them *once* in
`scripture_preprocess.py`, compute all pairwise similarities up front, and
persist the result.  `scripture_search.py` then loads that pre-computed matrix
and answers queries instantly — no model required at search time.

See the [Semantic Textual Similarity tutorial](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html)
for the full API documentation.

---

## Part 0 — Data

Download `book-of-mormon.json` from the
[scriptures-json](https://github.com/bcbooks/scriptures-json) repository
(raw URL:
`https://raw.githubusercontent.com/bcbooks/scriptures-json/master/book-of-mormon.json`)
and save it alongside your scripts, or in a `data/` subfolder.

The top-level structure of the file looks like this:

```json
{
  "books": [
    {
      "book": "1 Nephi",
      "chapters": [
        {
          "chapter": 1,
          "verses": [
            {
              "reference": "1 Nephi 1:1",
              "text": "I, Nephi, having been born of goodly parents …"
            }
          ]
        }
      ]
    }
  ]
}
```

Each verse object has two fields you need:

- `"reference"` — a human-readable citation, e.g. `"1 Nephi 1:1"`
- `"text"` — the verse text

---

## Part 1 — `scripture_preprocess.py`

This script runs **once** (it is slow).  It should:

1. **Load** `book-of-mormon.json` with the `json` module.
2. **Flatten** the nested structure into two parallel lists:
   - `references` — one string per verse, e.g. `["1 Nephi 1:1", "1 Nephi 1:2", …]`
   - `texts` — the corresponding verse texts
3. **Encode** every verse text with a `SentenceTransformer` model.

   ```python
   from sentence_transformers import SentenceTransformer

   model = SentenceTransformer("all-MiniLM-L6-v2")
   embeddings = model.encode(texts, show_progress_bar=True, convert_to_tensor=True)
   # embeddings.shape → (n_verses, 384)
   ```

4. **Compute the full similarity matrix** — every verse against every other verse.

   ```python
   similarity_matrix = model.similarity(embeddings, embeddings)
   # similarity_matrix.shape → (n_verses, n_verses)
   # similarity_matrix[i][j] is the cosine similarity between verse i and verse j
   ```

5. **Save** the similarity matrix and the reference list so `scripture_search.py`
   needs neither the model nor the raw embeddings:

   ```python
   import numpy as np, json

   np.save("bom_similarity.npy", similarity_matrix.numpy())
   with open("bom_references.json", "w") as f:
       json.dump(references, f)
   ```

6. **Print** a short summary when finished, e.g.:
   ```
   Encoded 6604 verses. Saved bom_similarity.npy (6604×6604) and bom_references.json.
   ```

> **Tip:** The Book of Mormon contains about 6,600 verses. Encoding them with
> `all-MiniLM-L6-v2` takes roughly 10–30 seconds on a CPU.  The resulting
> similarity matrix is about 175 MB on disk (6600 × 6600 × 4 bytes, float32).

---

## Part 2 — `scripture_search.py`

This script loads the pre-computed data and answers user queries — no model
needed.  It should:

1. **Load** the similarity matrix, the reference list, and build a text lookup
   from the original JSON (so you can display verse text in the results).

   ```python
   import numpy as np, json

   similarity_matrix = np.load("bom_similarity.npy")
   with open("bom_references.json") as f:
       references = json.load(f)

   # Also load verse texts for display
   with open("data/book-of-mormon.json") as f:
       bom = json.load(f)
   texts = [verse["text"]
            for book in bom["books"]
            for chapter in book["chapters"]
            for verse in chapter["verses"]]
   ```

2. **Build a lookup** from reference string to index:

   ```python
   ref_to_idx = {ref: i for i, ref in enumerate(references)}
   ```

3. **Enter a loop** that:
   - Prompts the user for a reference with `input()`, e.g.:
     ```
     Enter a Book of Mormon reference (or 'q' to quit): 1 Nephi 3:7
     ```
   - Looks up the index of the entered reference in `ref_to_idx`.  If the
     reference is not found, print a helpful message and continue.
   - **Reads the pre-computed row** of the similarity matrix for that verse:

     ```python
     scores = similarity_matrix[query_idx]   # shape: (n_verses,)
     ```

   - Finds the **top 11** indices by score (the query verse itself will be
     #1 with a score of 1.0, so you need 11 to get 10 *other* verses).

     ```python
     import numpy as np

     top_indices = np.argsort(scores)[::-1][:11]
     ```

   - Prints the results like this:

     ```
     Top 10 verses most similar to 1 Nephi 3:7:

      1. (0.8412)  1 Nephi 7:12  — Yea, and how is it that ye have forgotten …
      2. (0.8104)  2 Nephi 1:20  — And he hath said that: Inasmuch as ye shall …
      …
     10. (0.7231)  Alma 36:3     — And now, O my son Helaman, behold, thou art …
     ```

> **Tip:** `np.argsort` returns indices that sort the array in ascending order;
> reverse with `[::-1]` to get highest scores first.

---

## Suggested file layout

```
labs/
    scripture_preprocess.py   ← you write this (Part 1)
    scripture_search.py       ← you write this (Part 2)
data/
    book-of-mormon.json       ← downloaded from scriptures-json
    bom_similarity.npy        ← generated by scripture_preprocess.py  (~175 MB)
    bom_references.json       ← generated by scripture_preprocess.py
```

---

## Extensions (optional)

- Add the other standard works (`doctrine-and-covenants.json`, etc.) so the
  search spans all LDS scriptures.
- Let the user type free text (not just a reference) to find similar verses —
  encode the query string directly instead of looking it up.
- Replace `all-MiniLM-L6-v2` with a larger model (e.g. `all-mpnet-base-v2`)
  and compare the results.
- Store only the **top-K neighbours** per verse (e.g. as a dict of lists) instead
  of the full matrix, to reduce disk usage.  What is the smallest K that still
  gives reasonable results?
