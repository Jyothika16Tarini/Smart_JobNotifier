# Smart_JobNotifier
This project fetches real-time job listings from multiple web sources, processes and cleans the data, and presents it through a structured HTML-based interface. It helps users discover relevant job opportunities efficiently while laying the groundwork for advanced job matching and recommendations.

Features
Real-time job scraping using Python (Requests, BeautifulSoup)

Data cleaning, de-duplication, and structured job formatting

Interactive HTML interface with UI rendering for job listings

KNN-based job classification based on required skills and job roles

Scalable architecture for future semantic job matching using sentence embeddings

Supports notification integration for recommended jobs

Tech Stack
Python: Requests, BeautifulSoup, Scikit-learn

Frontend: HTML, CSS (basic UI rendering)

Algorithms: KNN classification, (extensible to sentence embeddings)

How It Works
Scrapes job data from real-time sources

Cleans and structures job details (title, skills, location, etc.)

Classifies jobs using KNN

Displays results in an HTML-based job listing page

Prepares for future extensions (semantic matching, recommendations)
