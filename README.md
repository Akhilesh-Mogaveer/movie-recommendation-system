# 🎬 Movie Recommendation System

A content-based movie recommendation engine using cosine similarity.

## Features
- Search 5000+ movies
- Get 5 personalized recommendations
- View movie posters from TMDB API
- Fast parallel poster fetching

## Installation

```bash
git clone <your-repo-url>
cd movie-recommendation-system
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Setup

1. Create `.env` file:
    TMDB_API_KEY=your_api_key_here

2. Run app:
```bash
streamlit run app.py
```

## Data Pipeline
TMDB Data → Feature Extraction → Stemming → Vectorization → Cosine Similarity → Streamlit

## Model Details
- **Features:** Genres, keywords, cast, director
- **Vectorization:** CountVectorizer (5000 features)
- **Similarity:** Cosine Similarity
- **Dataset:** TMDB 5000 Movies

## Deployment

Deployed on: [Streamlit Cloud Link]

## Author
**Akhilesh**
- [LinkedIn](https://linkedin.com/in/akhilesh-1109ma) | [GitHub](https://github.com/Akhilesh-Mogaveer)