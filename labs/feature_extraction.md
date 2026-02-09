# Feature extraction

Make a tab-separated values (tsv) file in the following format:

```
doc_id	feature1	feature2	feature3	...
doc1	0	1	0	...
doc2	1	0	1	...
doc3	0	1	1	...
```

doc_id can be a file path, an nltk corpus name + doc id, or any other unique
identifier for a document. Try to choose features that you think might be useful
for distinguishing between different genres or types of documents.

## Source corpora

You must use at least the following corpora, but you are welcome to use others if you are interested:

- poems (files in `corpora/poems/`)
- news (`nltk.corpus.treebank` or `nltk.corpus.reuters`)
- movie reviews (`nltk.corpus.movie_reviews`)
- twitter (`nltk.corpus.twitter_samples`)
