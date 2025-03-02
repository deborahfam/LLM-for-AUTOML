import requests
from bs4 import BeautifulSoup
import json
import re
import time
from tqdm import tqdm

# Configure headers and parameters
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
questions = []

def extract_metadata(text, tags):
    # Common problem types and metrics keywords
    problem_types = ['clustering', 'classification', 'regression', 'nlp', 
                    'computer-vision', 'recommendation', 'time-series']
    metrics_keywords = ['accuracy', 'precision', 'recall', 'f1 score', 'mae', 
                       'mse', 'rmse', 'auc-roc']
    data_keywords = ['images', 'text', 'csv', 'sensor data', 'tabular', 
                    'time-series', 'database']
    
    # Find problem type from tags
    problem_type = [tag for tag in tags if tag.lower() in problem_types]
    
    # Find metrics and data from text
    metrics = list(set([word for word in metrics_keywords if re.search(rf'\b{word}\b', text, re.I)]))
    required_data = list(set([word for word in data_keywords if re.search(rf'\b{word}\b', text, re.I)]))
    
    return {
        "problem_type": problem_type[0] if problem_type else "not specified",
        "metrics": metrics or ["not specified"],
        "required_data": required_data or ["not specified"]
    }

def scrape_stackoverflow(page=1):
    url = f"https://stackoverflow.com/questions/tagged/machine-learning?tab=votes&page={page}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for question in soup.select('.s-post-summary'):
        title = question.select_one('.s-post-summary--content-title').text.strip()
        tags = [tag.text for tag in question.select('.post-tag')]
        excerpt = question.select_one('.s-post-summary--content-excerpt').text.strip()
        user = question.select_one('.s-user-card--link').text.strip()
        response_count = question.select_one('.s-post-summary--stats-item-number').text.strip()
        votes = question.select_one('.s-post-summary--stats-item-number').text.strip()
        
        metadata = extract_metadata(f"{title} {excerpt}".lower(), tags)
        
        questions.append({
            "input": title,
            "metadata": metadata,
            "user": user,
            "response_count": response_count,
            "votes": votes,
            "tags": tags
        })
    
    # Respectful delay between requests
    time.sleep(2)

# Scrape first 2 pages (adjust as needed)
for page in tqdm(range(1, 10), desc="Scraping StackOverflow"):
    scrape_stackoverflow(page)

classification_questions = [q for q in questions if q["metadata"]["problem_type"]!="not specified"]

# Save to JSON
with open('ml_stackoverflow_questions.json', 'w') as f:
    json.dump(classification_questions, f, indent=2)

print("Scraping completed. Data saved to ml_stackoverflow_questions.json")