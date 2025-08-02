# scraper.py (Final working version)

import requests
from bs4 import BeautifulSoup
import json
import time
import sqlite3

def scrape_remoteok():
    url = 'https://remoteok.com/remote-dev-jobs'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    jobs = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr', class_='job')
        for row in rows:
            try:
                title = row.find('h2').text.strip()
                company = row.find('h3').text.strip()
                link = 'https://remoteok.com' + row['data-href']
                tags = [tag.text.strip().lower() for tag in row.find_all('div', class_='tag')]
                location = row.find('div', class_='location')
                location = location.text.strip() if location else "Remote"
                summary = title + " at " + company
                jobs.append({"title": title, "company": company, "location": location, "summary": summary, "tags": tags, "link": link})
            except Exception as e:
                print("RemoteOK job parsing error:", e)
    return jobs

def scrape_weworkremotely():
    url = 'https://weworkremotely.com/remote-jobs/search?term=developer'
    response = requests.get(url)
    jobs = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        sections = soup.find_all('section', class_='jobs')
        for section in sections:
            for li in section.find_all('li', class_='feature'):
                try:
                    link = 'https://weworkremotely.com' + li.find('a')['href']
                    company = li.find('span', class_='company').text.strip()
                    title = li.find('span', class_='title').text.strip()
                    location = li.find('span', class_='region company').text.strip() if li.find('span', class_='region company') else "Remote"
                    summary = title + " at " + company
                    jobs.append({"title": title, "company": company, "location": location, "summary": summary, "tags": [], "link": link})
                except Exception as e:
                    print("WWR job parsing error:", e)
    return jobs

def scrape_remotive():
    url = "https://remotive.io/api/remote-jobs"
    jobs = []
    try:
        response = requests.get(url)
        data = response.json()
        for job in data.get("jobs", []):
            title = job['title']
            company = job['company_name']
            location = job.get('candidate_required_location', 'Remote')
            summary = job['description'][:200].strip().replace('\n', ' ')
            tags = job['tags']
            link = job['url']
            jobs.append({"title": title, "company": company, "location": location, "summary": summary, "tags": [t.lower() for t in tags], "link": link})
    except Exception as e:
        print("Remotive error:", e)
    return jobs

def scrape_arbeitnow():
    url = 'https://www.arbeitnow.com/api/job-board-api'
    jobs = []
    try:
        response = requests.get(url)
        data = response.json()
        for job in data.get("data", []):
            title = job['title']
            company = job['company_name']
            location = job.get('location', 'Remote')
            summary = job.get('description', '')[:200].strip().replace('\n', ' ')
            tags = job.get("tags", [])
            link = job['url']
            jobs.append({"title": title, "company": company, "location": location, "summary": summary, "tags": [t.lower() for t in tags], "link": link})
    except Exception as e:
        print("Arbeitnow error:", e)
    return jobs

def scrape_jobspresso():
    url = "https://jobspresso.co/remote-developer-jobs/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    jobs = []
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('li', class_='job_listing')
        for post in posts:
            try:
                title = post.find('h3').text.strip()
                company = post.find('div', class_='job_listing-company').text.strip()
                location = post.find('div', class_='job_listing-location').text.strip() if post.find('div', class_='job_listing-location') else "Remote"
                link = post.find('a')['href']
                summary = title + " at " + company
                jobs.append({"title": title, "company": company, "location": location, "summary": summary, "tags": [], "link": link})
            except Exception as e:
                print("Jobspresso error:", e)
    except Exception as e:
        print("Jobspresso main error:", e)
    return jobs

def filter_by_skills(jobs, skills):
    skills = [skill.strip().lower() for skill in skills]
    filtered = []
    for job in jobs:
        combined = " ".join(job.get("tags", []) + [job.get("title", ""), job.get("summary", "")]).lower()
        if any(skill in combined for skill in skills):
            filtered.append(job)
    return filtered

def store_in_db(jobs):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (title TEXT, company TEXT, location TEXT, summary TEXT, tags TEXT, link TEXT)''')
    c.execute("DELETE FROM jobs")
    for job in jobs:
        try:
            c.execute("INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?)", (
                job['title'],
                job['company'],
                job['location'],
                job['summary'],
                ", ".join(job['tags']),
                job['link']
            ))
        except Exception as e:
            print("DB insert error:", e)
    conn.commit()
    conn.close()

def scrape_all(user_skills):
    all_jobs = []
    all_jobs += scrape_remoteok()
    all_jobs += scrape_weworkremotely()
    all_jobs += scrape_remotive()
    all_jobs += scrape_arbeitnow()
    all_jobs += scrape_jobspresso()

    print(f"Total scraped jobs: {len(all_jobs)}")

    filtered = filter_by_skills(all_jobs, user_skills)
    print(f"Filtered jobs by skills: {len(filtered)}")

    store_in_db(filtered)
    return filtered

if __name__ == "__main__":
    user_input = input("Enter your skills (comma separated): ")
    skills = [s.strip() for s in user_input.split(",") if s.strip()]
    jobs = scrape_all(skills)
    print(f"{len(jobs)} jobs stored in DB matching skills: {skills}")
