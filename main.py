import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout='wide'
)

# Get your own API Key
OMDb_api_key = "xxxxxxxx"


def fetch_details(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDb_api_key}"
    data = requests.get(url)
    response = data.json()
    return{
        "title": response.get("Title", movie_title),
        "poster": response.get("Poster", "N/A"),
        "year": response.get("Year", "N/A"),
        "genre": response.get("Genre", "N/A"),
        "rating": response.get("imdbRating", "N/A")
    }


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    recommendations = []
    for item in movie_list:
        recommendations.append(fetch_details(movies.iloc[item[0]].title))
    return recommendations


movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

st.markdown(
    "<h1 style='text-align:center;'>🎬 Movie Recommender System</h1>",
    unsafe_allow_html=True
)

st.write("")

selected_movie_name = st.selectbox(
    "Which movie have you recently watched?",
    movies['title'].values
)

selected_movie = fetch_details(selected_movie_name)
col1, col2 = st.columns([1,3])

with col1:
    st.image(selected_movie["poster"])

with col2:
    st.subheader(selected_movie["title"])
    st.write(f" ⭐ IMDb Rating: {selected_movie['rating']}")
    st.write(f" 📅 Year: {selected_movie['year']}")
    st.write(f" 🎭 Genre: {selected_movie['genre']}")

st.write("")


if st.button('Recommend'):
    with st.spinner("Getting best movies..."):
        recommend_movies = recommend(selected_movie_name)

    st.markdown("## Recommended Movies For You")
    cols = st.columns(5)

    for idx, movie in enumerate(recommend_movies):
        with cols[idx]:
            if movie['poster'] != 'N/A':
                st.image(movie['poster'])
            else:
                st.text("POSTER NOT AVAILABLE CURRENTLY")
            st.write(movie['title'])
            st.write("")
            st.write(f"⭐ Rating: ", movie['rating'])
            st.write(f"🎭 Genre: ", movie['genre'])