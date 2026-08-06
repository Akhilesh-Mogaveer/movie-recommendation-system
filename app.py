import streamlit as st
import pandas as pd
import pickle
import requests
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from huggingface_hub import hf_hub_download

load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')


REPO_ID = "Akhileshh1/movie-recommendation-system"

@st.cache_resource
def download_files():
    if not os.path.exists("movies_dict.pkl"):
        hf_hub_download(
            repo_id=REPO_ID,
            filename="movies_dict.pkl",
            local_dir="."
        )

    if not os.path.exists("similarity.pkl"):
        hf_hub_download(
            repo_id=REPO_ID,
            filename="similarity.pkl",
            local_dir="."
        )



@st.cache_data
def fetch_poster(movie_id):
    """Fetch poster from TMDB."""
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US'
    placeholder = "https://via.placeholder.com/500x750?text=No+Image"

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            poster_path = response.json().get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return placeholder
        except requests.exceptions.RequestException:
            if attempt == 2:
                return placeholder
    return placeholder


@st.cache_data
def load_models():
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity


def recommend(movie, movies, similarity):
    try:
        movie_index = movies[movies["title"] == movie].index[0]
    except IndexError:
        st.error(f"Movie '{movie}' not found!")
        return None, None

    distances = similarity[movie_index]
    movie_list = sorted(
        enumerate(distances),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    movie_ids = []

    for idx, _ in movie_list:
        recommended_movies.append(movies.iloc[idx]["title"])
        movie_ids.append(movies.iloc[idx]["movie_id"])

    
    recommended_posters = [None] * len(movie_ids)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(fetch_poster, mid): i
            for i, mid in enumerate(movie_ids)
        }

        for future in as_completed(futures):
            index = futures[future]
            recommended_posters[index] = future.result()

    return recommended_movies, recommended_posters



st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title('🎬 Movie Recommendation System')


download_files()

movies, similarity = load_models()

selected_movie = st.selectbox("Choose a movie", movies["title"].values)

if st.button("Recommend", type="primary"):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie, movies, similarity)

    if names:
        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.image(poster, use_column_width=True)
                st.caption(name)