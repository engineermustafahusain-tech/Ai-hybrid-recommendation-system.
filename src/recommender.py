import os
import pandas as pd
import requests
from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# LOAD DATA (PATH SAFE)
# --------------------------------------------------
BASE_DIR = os.path.dirname(__file__)

movies = pd.read_csv(os.path.join(BASE_DIR, "movies.csv"))
ratings = pd.read_csv(os.path.join(BASE_DIR, "ratings.csv"))
links = pd.read_csv(os.path.join(BASE_DIR, "links.csv"))

# --------------------------------------------------
# CONTENT-BASED MODEL
# --------------------------------------------------
movies["genres"] = movies["genres"].str.replace("|", " ", regex=False)

tfidf = TfidfVectorizer()
movie_tfidf = tfidf.fit_transform(movies["genres"])
content_similarity = cosine_similarity(movie_tfidf)

# --------------------------------------------------
# COLLABORATIVE FILTERING (ITEM-BASED)
# --------------------------------------------------
user_movie_matrix = ratings.pivot_table(
    index="userId",
    columns="movieId",
    values="rating"
)

movie_user_matrix = user_movie_matrix.T.fillna(0)
collab_similarity = cosine_similarity(movie_user_matrix)

collab_similarity_df = pd.DataFrame(
    collab_similarity,
    index=movie_user_matrix.index,
    columns=movie_user_matrix.index
)

# --------------------------------------------------
# TMDB CONFIG
# --------------------------------------------------
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

@lru_cache(maxsize=500)
def fetch_poster_url(tmdb_id):
    if pd.isna(tmdb_id) or TMDB_API_KEY is None:
        return None

    try:
        url = f"https://api.themoviedb.org/3/movie/{int(tmdb_id)}"
        params = {"api_key": TMDB_API_KEY}
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        pass

    return None

# --------------------------------------------------
# HYBRID RECOMMENDATION (USER BASED)
# --------------------------------------------------
def hybrid_recommend(user_id, top_n=10, alpha=0.6):
    liked_movies = ratings[
        (ratings["userId"] == user_id) & (ratings["rating"] >= 4)
    ]["movieId"]

    if liked_movies.empty:
        return pd.DataFrame(columns=["title", "genres", "tmdbId"])

    watched = set(ratings[ratings["userId"] == user_id]["movieId"])
    scores = {}

    for movie_id in liked_movies:
        # Collaborative
        if movie_id in collab_similarity_df:
            for sim_movie, score in collab_similarity_df[movie_id].items():
                scores[sim_movie] = scores.get(sim_movie, 0) + alpha * score

        # Content-based
        idx = movies[movies["movieId"] == movie_id].index
        if len(idx) > 0:
            idx = idx[0]
            for i, score in enumerate(content_similarity[idx]):
                sim_movie_id = movies.iloc[i]["movieId"]
                scores[sim_movie_id] = scores.get(sim_movie_id, 0) + (1 - alpha) * score

    recommended_ids = [
        mid for mid in sorted(scores, key=scores.get, reverse=True)
        if mid not in watched
    ][:top_n]

    result = movies[movies["movieId"].isin(recommended_ids)]
    result = result.merge(links[["movieId", "tmdbId"]], on="movieId", how="left")

    return result[["title", "genres", "tmdbId"]]

# --------------------------------------------------
# RECOMMEND BY MOVIE NAME (ITEM-TO-ITEM)
# --------------------------------------------------
def recommend_by_movie_title(movie_title, top_n=10):
    match = movies[movies["title"].str.contains(movie_title, case=False, na=False)]

    if match.empty:
        return pd.DataFrame(columns=["title", "genres", "tmdbId"])

    movie_idx = match.index[0]

    similarity_scores = list(enumerate(content_similarity[movie_idx]))
    similarity_scores = sorted(
        similarity_scores, key=lambda x: x[1], reverse=True
    )[1:top_n+1]

    movie_indices = [i[0] for i in similarity_scores]

    result = movies.iloc[movie_indices]
    result = result.merge(links[["movieId", "tmdbId"]], on="movieId", how="left")

    return result[["title", "genres", "tmdbId"]]

# --------------------------------------------------
# TRENDING MOVIES (LAST 30 DAYS)
# --------------------------------------------------
def get_trending_movies(days=30, top_n=20):
    ratings_copy = ratings.copy()
    ratings_copy["date"] = pd.to_datetime(ratings_copy["timestamp"], unit="s")

    cutoff_date = ratings_copy["date"].max() - pd.Timedelta(days=days)
    last_x_days = ratings_copy[ratings_copy["date"] >= cutoff_date]

    movie_stats = last_x_days.groupby("movieId").agg(
        avg_rating=("rating", "mean"),
        rating_count=("rating", "count"),
        latest_rating_time=("date", "max")
    ).reset_index()

    movie_stats["trending_score"] = (
        movie_stats["avg_rating"] * movie_stats["rating_count"]
    )

    top_movies = movie_stats.sort_values(
        by=["trending_score", "latest_rating_time"],
        ascending=False
    ).head(top_n)

    top_movies = (
        top_movies
        .merge(movies[["movieId", "title", "genres"]], on="movieId")
        .merge(links[["movieId", "tmdbId"]], on="movieId", how="left")
    )

    return top_movies[["title", "genres", "avg_rating", "rating_count", "tmdbId"]]
