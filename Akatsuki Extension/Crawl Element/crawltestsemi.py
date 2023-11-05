from bs4 import BeautifulSoup as bs
import requests 
requests.urllib3.disable_warnings()
from urllib.parse import urlparse
import certifi
import urllib3



class Cubdo:
    def __init__(self, tgl=None, out=None):
        self.path = f"domains-registered-by-date/{tgl}/"
        self.outs = out
        self.outs = open(out, "a") if out else None
        self.tots = 0

        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    
    def gas(self, path=""):
        session = requests.Session()
        session.verify = False
        respon = session.get(f"https://66.45.249.94/{path}", headers={'Host': 'www.cubdomain.com'}, timeout=30).text
        
        return respon
    
    def gasken(self):
        try:
            raw = self.gas(self.path + "1")
            self.ambil(raw, "1")
            pagination_ul = bs(raw, "html.parser").find("ul", {"class": "pagination-sm pagination mb-0 mt-2"})

            if pagination_ul:
                pages = pagination_ul.findAll("a")[-2].text.strip()
                for i in range(2, int(pages) + 1):
                    self.ambil(self.gas(self.path + str(i)), i)

            # Call the ambil method to save the scraped data to domain_log.txt
            print("\nDone, total domains:", self.tots)
            print("Thanks for using this tool!\n")
        except KeyboardInterrupt:
            print("Killed!")
            exit()

    def ambil(self, raw, hal):
        items = bs(raw, "html.parser").findAll("div", {"class": "col-md-4"})
        log_filename = "domain_log.txt"
        
        with open(log_filename, "a") as log_file:
            log_file.write(f"Page {hal} found {len(items)} domains\n")
            
            self.tots += len(items)
            for item in items:
                domain = item.a.text.strip()
                # Extract site_name and process it
                log_file.write(f"https://{domain}\n")

    def save_to_domain_log(self):
        log_filename = "domain_log.txt"

        with open(log_filename, "a") as log_file:
            log_file.write(f"Total domains scraped for date {self.outs}: {self.tots}\n")
    
    def extract_site_name_and_process(self, domain):
        parsed_url = urlparse(domain)
        if parsed_url.scheme and parsed_url.netloc:
            path = parsed_url.path
            path_components = path.split('/')
            if len(path_components) >= 3 and path_components[1] == 'site':
                site_name = path_components[2]
                print("Extracted site_name:", site_name)
                
                # Implement your phishing detection or prediction logic here using 'site_name'
                # For now, printing a placeholder message
                print("Phishing detection or prediction for site_name:", site_name)
        

# Example usage
date = None
WEBSITE_URL = f"https://www.cubdomain.com/domains-registered-by-date/{date}/1"
cubdo = Cubdo(tgl=date)
cubdo.gasken()
