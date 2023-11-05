import requests
import time

WEBSITE_URL = "http://127.0.0.1:5500/index.html"  # Change this to your target website URL
CRAWL_DEPTH = 3

PREDICTION_API_URL = "https://0c6d-35-243-190-28.ngrok-free.app/predict"
PHISHING_API_URL = "https://phishing-website-detection-production.up.railway.app/api/detect2/"

BATCH_SIZE = 10  # Number of links to process in each batch
MALICIOUS_THRESHOLD = 70  # Malicious probability threshold

def get_urls_from_file(file_path):
    with open(file_path, "r") as log_file:
        urls = [line.strip() for line in log_file if line.startswith("https://")]
    return urls

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
    urls = get_urls_from_file("domain_log.txt")
    malicious_links = []

    for url in urls:
        malicious_probability = predict_malicious_prob(url)
        print(f"Malicious probability of {url}: {malicious_probability}")

        if malicious_probability > MALICIOUS_THRESHOLD:
            malicious_links.append(url)
            if len(malicious_links) >= BATCH_SIZE:
                print("Sending batch to phishing detection API...")
                results = check_phishing_batch(malicious_links)
                for url, result in zip(malicious_links, results):
                    if result:
                        print(f"{url} confirmed Malicious")
                        with open("Confirmed_Malicious.txt", "a") as file:
                            file.write(f"{url}\n")
                    else:
                        print(f"{url} is safe.")
                malicious_links = []
                break

    print("Checking completed.")
