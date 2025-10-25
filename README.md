# 🎬 Movie Recommender System (Content-Based Filtering with Bag of Words)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://movie-recommenderbow.streamlit.app/)

Welcome to the Movie Recommender System! This project leverages **Content-Based Filtering** combined with the **Bag of Words (BoW)** text representation technique to suggest movies similar to the ones you like. Built with Python, Scikit-learn, and Streamlit, it provides an interactive way to explore movie recommendations based on their core content.

[Image of a modern movie recommender interface]

## ✨ Features

* **Content-Based Recommendations:** Suggests movies based on similarity in plot, genre, keywords, main actors, and director.
* **Bag of Words (BoW) Model:** Utilizes `CountVectorizer` from Scikit-learn to convert processed text data into a matrix of token counts.
* **Cosine Similarity:** Measures the similarity between movies based on the angle between their BoW vectors in a high-dimensional space.
* **Interactive Web UI:** A user-friendly interface built with Streamlit allowing users to select a movie and instantly get recommendations.
* **Dynamic Poster Fetching:** Integrates with The Movie Database (TMDB) API to display movie posters.

## 🚀 Live Demo

Experience the recommender system live: \
[**Try the Movie Recommender App!**](https://movie-recommenderbow.streamlit.app/)

## 💡 How It Works: The Pipeline

This recommender system follows a systematic approach:

1.  **Data Loading & Merging:** Loads movie metadata and credits information from datasets (e.g., TMDB 5000 dataset). Merges relevant information into a single DataFrame.
2.  **Feature Selection:** Selects key features crucial for content-based filtering: `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, and `crew`.
3.  **Data Preprocessing & Feature Engineering:**
    * Extracts relevant information (e.g., top 3 actors from `cast`, director from `crew`).
    * **Crucially, removes spaces** from multi-word names (e.g., "Science Fiction" becomes "ScienceFiction", "Tom Holland" becomes "TomHolland") to treat them as unique entities.
    * (Optional but recommended in the original tutorial: Applies stemming to reduce words to their root form, e.g., "actions" and "action" both become "action").
    * Combines these processed features into a single comprehensive `tags` string for each movie.
4.  **Text Vectorization (Bag of Words):**
    * The `tags` column, containing all descriptive text for each movie, is processed using Scikit-learn's `CountVectorizer`.
    * This converts the text corpus into a large matrix where:
        * Each **row** represents a movie.
        * Each **column** represents a unique word (token) from the entire corpus (limited to the top 5000 most frequent words, excluding English stop words like "and", "the", etc.).
        * The **value** in cell `(i, j)` is the count of how many times word `j` appears in the `tags` for movie `i`.
    * This matrix numerically represents the content of each movie.
5.  **Similarity Calculation:**
    * **Cosine Similarity** is calculated between all pairs of movie vectors in the BoW matrix.
    * This yields a similarity matrix where `similarity[i][j]` is a score between 0 and 1 indicating how similar movie `i` is to movie `j` based on their shared words/tags. A score of 1 means identical content (based on BoW), and 0 means no shared content.
6.  **Recommendation Generation:**
    * When a user selects a movie, the system finds its index.
    * It retrieves the row corresponding to that movie from the similarity matrix. This row contains the similarity scores between the selected movie and all other movies.
    * The scores are sorted in descending order.
    * The indices of the top 5 highest scores (excluding the movie itself) are selected.
    * The titles and posters (via TMDB API) corresponding to these indices are fetched and displayed.
7.  **Frontend Display:** Streamlit is used to create the select box, button, and display the recommended movie titles and posters in neat columns.

## 🛠️ Tech Stack

* **Core:** Python 3.x
* **Data Handling:** Pandas
* **Machine Learning/NLP:** Scikit-learn (`CountVectorizer`, `cosine_similarity`)
* **Web Framework:** Streamlit
* **API Interaction:** Requests
* **Object Serialization:** Pickle (for loading precomputed data/model)

## ⚙️ Local Setup

Follow these steps to run the project on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Krish00711/Movie-Recommender-BOW-.git](https://github.com/Krish00711/Movie-Recommender-BOW-.git)
    cd Movie-Recommender-BOW-
    ```
2.  **Set up a Python virtual environment (highly recommended):**
    ```bash
    python -m venv venv
    # Activate the environment
    #
