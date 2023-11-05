import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from collections import deque
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# Delay between requests to avoid overloading the server
REQUEST_DELAY = 1  # in seconds

WEBSITE_URL = "http://127.0.0.1:5500/index.html"  # Change this to your target website URL
CRAWL_DEPTH = 3

PREDICTION_API_URL = "https://093b-34-85-130-180.ngrok-free.app/predict"
PHISHING_API_URL = "https://phishing-website-detection-production.up.railway.app/api/detect2/"

# uri = "mongodb+srv://<username>:<password>@cluster0.vv9yrxd.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# db = client['Crawled_Phishes']  # Replace with your database name
# collection = db['malicious_urls']  # Replace with your collection name

BATCH_SIZE = 10  # Number of links to process in each batch
MALICIOUS_THRESHOLD = 70  # Malicious probability threshold


def get_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []

        for anchor in soup.find_all('a'):
            href = anchor.get('href')
            if href:
                absolute_url = urljoin(url, href)
                parsed_url = urlparse(absolute_url)
                if parsed_url.scheme and parsed_url.netloc:
                    links.append(absolute_url)

        return links
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def predict_malicious_prob(url):
    try:
        response = requests.post(PREDICTION_API_URL, json={"url": url})
        response.raise_for_status()
        json_response = response.json()
        return json_response.get("malicious_probability", 0)
    except requests.exceptions.RequestException as e:
        print(f"Error predicting malicious probability: {e}")
        return 0

def check_phishing_batch(urls):
    results = []
    
    for url in urls:
        try:
            response = requests.post(PHISHING_API_URL, json={"url": url})
            response.raise_for_status()
            json_response = response.json()
            result = json_response.get("result", False)
            results.append(result)
        except requests.exceptions.RequestException as e:
            print(f"Error checking phishing for {url}: {e}")
            results.append(False)
    
    return results


if __name__ == "__main__":
    url_queue = deque()
    url_queue.append(WEBSITE_URL)

    visited_links = set()
    malicious_links = []

    while url_queue and len(malicious_links) < 10:
        current_url = url_queue.popleft()
        visited_links.add(current_url)

        links = get_links(current_url)

        for link in links:
            if link not in visited_links:
                url_queue.append(link)
                time.sleep(REQUEST_DELAY)  # Introduce delay to be respectful

                malicious_probability = predict_malicious_prob(link)
                print(f"Malicious probability of {link}: {malicious_probability}")

                if malicious_probability > MALICIOUS_THRESHOLD:
                    malicious_links.append(link)
                    if len(malicious_links) >= BATCH_SIZE:
                        print("Sending batch to phishing detection API...")
                        results = check_phishing_batch(malicious_links)
                        for url, result in zip(malicious_links, results):
                            if result:
        
                                print(f"{url} confirmed Malicious")
                            else:
                                print(f"{url} is safe.")
                        malicious_links = []  # Clear the batch

    print("Crawling and checking completed.")
