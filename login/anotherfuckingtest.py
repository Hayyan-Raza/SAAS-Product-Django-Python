import json
import requests
import os

# Load your API key from environment variables
PAGESPEED_API_KEY = os.getenv('PAGESPEED_API_KEY')

def fetch_pagespeed_data(url):
    api_url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
    params = {
        'url': url,
        'category': ['performance', 'accessibility', 'best-practices', 'seo', 'pwa'],
        'key': PAGESPEED_API_KEY
    }
    response = requests.get(api_url, params=params)
    return response.json()

def extract_category_scores(data):
    categories = data.get('lighthouseResult', {}).get('categories', {})
    scores = {}
    for category, details in categories.items():
        score = details.get('score')
        if score is not None:
            scores[category] = round(score * 100, 2)  # Convert to percentage
    return scores

def print_scores(scores):
    print("PageSpeed Insights Scores:")
    for category, score in scores.items():
        print(f"{category.capitalize()}: {score}%")





if __name__ == "__main__":
    url = 'https://www.monday.com'  # Replace with your target URL
    data = fetch_pagespeed_data(url)
    scores = extract_category_scores(data)
    print_scores(scores)
