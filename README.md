🎬 Hybrid Movie Recommendation System (Netflix-Style)

A Netflix-style hybrid movie recommendation system that combines content-based filtering, collaborative filtering, and trending logic to deliver personalized and engaging movie recommendations.
The application is built using Python and Streamlit, deployed on Hugging Face Spaces, and enhanced with TMDB movie posters for a real OTT-like experience.

🚀 Live Demo

👉 Hugging Face App
https://huggingface.co/spaces/engineermustafahusain/hybrid-movie-recommender

🎯 Project Goal

The primary goal of this project is to simulate how real streaming platforms like Netflix recommend content by:

Solving the movie discovery problem

Providing personalized recommendations

Handling cold-start users

Combining multiple recommendation strategies

Deploying a production-style ML web application

Following secure API and deployment practices

This project is designed as proof of real-world recommendation system understanding, not a toy example.

🧠 Business Logic (Proof of Work)
1️⃣ Trending Movies (Cold-Start Solution)

Problem: New users have no history
Solution: Show trending content

Logic:

Filter ratings from last 30 days

Compute:

Average rating

Rating count

Latest interaction time

Trending score:

Trending Score = Average Rating × Rating Count


Business Value:
Works for everyone, increases engagement, mimics “Trending Now”.

2️⃣ Content-Based Filtering

Problem: Users prefer similar types of movies
Solution: Recommend similar movies based on genres

Logic:

Convert genres into text

Apply TF-IDF

Compute cosine similarity

Business Value:
Explainable and stable recommendations.

3️⃣ Collaborative Filtering

Problem: Users like what similar users like
Solution: Item-based collaborative filtering

Logic:

User-movie rating matrix

Item-to-item similarity

Community behavior learning

Business Value:
Captures hidden preferences and diversity.

4️⃣ Hybrid Recommendation Engine (Core Logic)

Instead of relying on a single method, the system uses a weighted hybrid approach.

🔢 Hybrid Weight Distribution
Component	Weight
Collaborative Filtering	60%
Content-Based Filtering	35%
Trending Boost	5%
📐 Final Scoring Formula
Final Score =
(0.60 × Collaborative Score)
+ (0.35 × Content Similarity Score)
+ (0.05 × Trending Score)


Why 5% Trending?

Encourages exploration

Prevents popularity bias

Improves long-term engagement

This balances personalization + stability + discovery.

5️⃣ Movie-to-Movie Recommendation

“Because you watched…”

User enters a movie name

System recommends similar movies

No login required

Business Value:
High engagement, easy discovery.

6️⃣ Visual Experience (TMDB Posters)

Uses tmdbId to fetch posters

Posters cached for performance

Netflix-style stable grid UI

User (Browser)
      ↓
Streamlit Web App (Hugging Face)
      ↓
Recommendation Engine
  ├─ Trending Logic
  ├─ Content-Based Model
  ├─ Collaborative Model
  └─ Hybrid Scoring
      ↓
MovieLens Dataset
      ↓
TMDB API (Posters)



📊 Model Evaluation Metrics (Short)

Because recommendation is a ranking problem, traditional accuracy is not enough.

Precision@K – relevance of recommendations

Recall@K – coverage of user preferences

F1-Score@K – balance between precision & recall

MAP (Mean Average Precision) – ranking quality

Coverage – diversity of recommendations

Cold-Start Performance – effectiveness for new users

🛠️ Tech Stack

Python

Pandas

Scikit-learn

Streamlit

TMDB API

Hugging Face Spaces

GitHub

📂 Project Structure
src/
 ├── streamlit_app.py
 ├── recommender.py
 ├── movies.csv
 ├── ratings.csv
 ├── links.csv
 └── __init__.py

requirements.txt
README.md

🔐 Environment Variables

API keys are handled securely.

Hugging Face
TMDB_API_KEY = your_api_key

Local (Optional)

Windows

setx TMDB_API_KEY "your_api_key"


Linux / macOS

export TMDB_API_KEY="your_api_key"

▶️ Run Locally
git clone https://github.com/engineermustafahusain-tech/Ai-hybrid-recommendation-system
cd Ai-hybrid-recommendation-system
pip install -r requirements.txt
streamlit run src/streamlit_app.py

📈 Future Improvements

User authentication

Explanation: “Why recommended?”

Dark Netflix theme

FastAPI backend

Docker & AWS deployment

A/B testing of hybrid weights

🎓 Learning Outcomes

Designed a real-world hybrid recommender system

Implemented cold-start handling

Applied ranking-based evaluation metrics

Deployed an ML app with secure secrets

Followed industry-standard architecture

👤 Author

Syed Mustafa Husain
Data Science & ML Enthusiast
GitHub: https://github.com/engineermustafahusain-tech

⭐ Acknowledgements

MovieLens Dataset

TMDB API

Hugging Face Spaces

⭐ If you find this project useful, give it a star!
