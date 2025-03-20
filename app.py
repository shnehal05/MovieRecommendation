import streamlit as st
import pickle
import pandas as pd
import os
import gdown  # To download from Google Drive

# Get the directory where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Updated Google Drive file link and ID
GOOGLE_DRIVE_FILE_ID = "1P8qbTjbD5sQtlbmcgBLtqkIdHxMGY1Ij"
SIMILARITY_PATH = os.path.join(BASE_DIR, 'similarity.pkl')

# Download similarity.pkl if not found
if not os.path.exists(SIMILARITY_PATH):
    st.info("Downloading required file: similarity.pkl...")
    gdown.download(f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}", SIMILARITY_PATH, quiet=False)

# Load pickle files safely
try:
    movies1 = pickle.load(open(os.path.join(BASE_DIR, 'movies.pkl'), 'rb'))  # DataFrame
    movies_list = pickle.load(open(os.path.join(BASE_DIR, 'movies_list.pkl'), 'rb'))  # List of titles
    similarity = pickle.load(open(SIMILARITY_PATH, 'rb'))  # NumPy array or list
except FileNotFoundError:
    st.error("One or more required files (movies.pkl, movies_list.pkl, similarity.pkl) are missing!")
    st.stop()

def recommend(movie):
    if movie not in movies_list:
        return ["Movie not found in the database."]
    
    movie_index = movies1[movies1['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommended = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    return [movies1.iloc[i[0]].title for i in recommended]

# Streamlit UI
st.title("🎬 Movie Recommender")
st.write("Find similar movies based on your last watched one! 🎥")

selected_movie = st.selectbox("Enter your last seen movie:", movies_list)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    st.subheader("You might also like:")
    for movie in recommendations:
        st.write(f"🎥 {movie}")
