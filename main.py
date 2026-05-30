import streamlit as st
import pickle
import pandas as pd

st.markdown("""
<style>
html, body, [class*="st-"] {
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    result = []
    for item in movie_list:
        result.append(movies.iloc[item[0]].title)
    return result


movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movie Recommender System")
print(type(movies_dict))
selected_movie_name = st.selectbox(
    "Which movie u recently watched?",
    movies['title'].values
)

if st.button('Recommend'):
    recommend_movie_list = recommend(selected_movie_name)
    for i in recommend_movie_list:
        st.write(i)