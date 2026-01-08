import sys
import os
import streamlit as st

BASE_DIR = os.path.dirname(__file__)
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from recommender import (
    get_trending_movies,
    hybrid_recommend,
    recommend_by_movie_title,
    fetch_poster_url
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")
st.write("Netflix-style Trending + Hybrid + Movie-based recommendations")

# ==================================================
# 🔥 TRENDING MOVIES
# ==================================================
st.header("🔥 Trending Movies (Last 30 Days)")

trending_df = get_trending_movies()

cols = st.columns(5)
for i, (_, row) in enumerate(trending_df.iterrows()):
    with cols[i % 5]:
        poster = fetch_poster_url(row["tmdbId"])
        if poster:
            st.image(poster, width=180)
        st.caption(row["title"])

# ==================================================
# 🎯 USER-BASED HYBRID
# ==================================================
st.divider()
st.header("🎯 Recommendations for User")

user_id = st.number_input("Enter User ID", min_value=1, step=1)

if st.button("Recommend for User"):
    results = hybrid_recommend(user_id)

    cols = st.columns(5)
    for i, (_, row) in enumerate(results.iterrows()):
        with cols[i % 5]:
            poster = fetch_poster_url(row["tmdbId"])
            if poster:
                st.image(poster, width=180)
            st.caption(row["title"])

# ==================================================
# 🎞️ MOVIE NAME BASED RECOMMENDATION
# ==================================================
st.divider()
st.header("🎞️ Recommend by Movie Name")

movie_name = st.text_input("Enter movie name (e.g. Inception)")

if st.button("Recommend Similar Movies"):
    results = recommend_by_movie_title(movie_name)

    if results.empty:
        st.warning("Movie not found.")
    else:
        cols = st.columns(5)
        for i, (_, row) in enumerate(results.iterrows()):
            with cols[i % 5]:
                poster = fetch_poster_url(row["tmdbId"])
                if poster:
                    st.image(poster, width=180)
                st.caption(row["title"])
