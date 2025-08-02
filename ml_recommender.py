# ml_recommender.py

import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Define role-based keywords you want to classify (customize this list as needed)
ML_ROLE_KEYWORDS = [
    'machine learning', 'ml engineer', 'artificial intelligence', 'deep learning',
    'data scientist', 'ai engineer', 'nlp engineer', 'computer vision'
]

def is_ml_related(text):
    """
    Checks if the job text is related to ML roles.
    """
    text = text.lower()
    return any(keyword in text for keyword in ML_ROLE_KEYWORDS)

def get_top_recommendations(user_skills, top_n=10):
    """
    Uses TF-IDF + cosine similarity to find top N job matches,
    prioritizing ML-related job roles.
    """
    user_skills_text = " ".join(user_skills).lower()

    # Connect and fetch job data
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT title, company, location, summary, tags, link FROM jobs")
    rows = c.fetchall()
    conn.close()

    jobs = []
    corpus = []

    for row in rows:
        title, company, location, summary, tags, link = row
        combined_text = f"{title} {summary} {tags}".lower()
        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "summary": summary,
            "tags": tags,
            "link": link,
            "text": combined_text
        })
        corpus.append(combined_text)

    if not jobs:
        return []

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    job_vectors = vectorizer.fit_transform(corpus)
    user_vector = vectorizer.transform([user_skills_text])

    # Compute cosine similarity
    similarities = cosine_similarity(user_vector, job_vectors).flatten()

    # Combine similarity and ML relevance
    ranked_jobs = []
    for idx, job in enumerate(jobs):
        score = similarities[idx]
        if is_ml_related(job['text']):
            score *= 1.5  # boost ML-related jobs
        ranked_jobs.append((job, score))

    # Sort by score
    ranked_jobs.sort(key=lambda x: x[1], reverse=True)

    # Return top N
    top_jobs = [job for job, _ in ranked_jobs[:top_n]]
    return top_jobs

# Test usage
if __name__ == "__main__":
    user_input = input("Enter your skills (comma separated): ")
    skills = [s.strip().lower() for s in user_input.split(",") if s.strip()]
    results = get_top_recommendations(skills)

    print(f"\nTop Recommended ML-related Jobs:\n")
    for job in results:
        print(f"- {job['title']} at {job['company']} ({job['location']})")
        print(f"  Tags: {job['tags']}")
        print(f"  Link: {job['link']}\n")
