# Spotify Genre Classifier

A data pipeline and unsupervised machine learning project that uses the Spotify Web API to classify artists by genre and surface micro-genre patterns across large-scale playlist data. Read the [write-up](https://abhilashatandon.com/blog/spotify-vis/) on my blog or see the [interactive visualization](https://abhilashatandon.com/projects/spotify_artists/). 

## Overview

This project retrieves playlist and listener behavior data from the Spotify API, processes audio features and metadata for 300,000+ songs, and applies unsupervised clustering techniques to classify 6,000+ artists by genre. The goal is to go beyond Spotify's genre labels and identify niche micro-genres based on patterns in the data.

## Methodology

The pipeline is structured in stages:

1. **Data Ingestion** — Retrieves track, artist, and audio feature data from the Spotify Web API with robust error handling and rate limit management.
2. **Feature Engineering** — Processes raw API responses into a clean, analysis-ready dataset using Pandas and NumPy.
3. **Similarity & Vectorization** — Applies TF-IDF and cosine similarity to represent relationships between artists based on shared playlist co-occurrence and genre tag overlap.
4. **Dimensionality Reduction** — Uses UMAP to reduce high-dimensional feature representations to a lower-dimensional embedding suitable for clustering.
5. **Clustering** — Applies spectral clustering to the reduced embeddings to group artists into genre and micro-genre clusters.

## Note

This project was built against an earlier version of the Spotify Web API and is not expected to run without modification, as Spotify has since changed how their API works. The repository is preserved as a reference for the methodology and implementation.

## Tech Stack

- **Language:** Python
- **Data & ML:** NumPy, Pandas, scikit-learn, UMAP
- **API:** Spotify Web API (via REST)

## License

[MIT](LICENSE)
