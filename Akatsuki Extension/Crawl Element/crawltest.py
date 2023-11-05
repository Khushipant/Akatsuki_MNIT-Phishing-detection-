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


date = "2023-08-08"
WEBSITE_URL = f"https://www.cubdomain.com/domains-registered-by-date/{date}/1"  # Change this to your target website URL
PREDICTION_API_URL = "https://093b-34-85-130-180.ngrok-free.app/predict"
PHISHING_API_URL = "https://phishing-website-detection-production.up.railway.app/api/detect2/"
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

                    path = parsed_url.path
                    path_components = path.split('/')
                    site_name = path_components[-1]
                    print(site_name)

        return links
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []
    
get_links(WEBSITE_URL)