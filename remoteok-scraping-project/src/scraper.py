import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
import os
import logging
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

class RemoteOKScraper:
    BASE_URL = "https://remoteok.com"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 RemoteOK-Scraper-Educational"
    
    # Expanded categories to maximize data yield
    CATEGORIES = [
        "remote-jobs", "remote-dev-jobs", "remote-engineer-jobs", "remote-exec-jobs",
        "remote-senior-jobs", "remote-developer-jobs", "remote-finance-jobs",
        "remote-sysadmin-jobs", "remote-java-jobs", "remote-golang-jobs",
        "remote-cloud-jobs", "remote-linux-jobs", "remote-sql-jobs",
        "remote-excel-jobs", "remote-ops-jobs", "remote-security-jobs",
        "remote-product-jobs", "remote-recruiter-jobs", "remote-hr-jobs",
        "remote-python-jobs", "remote-javascript-jobs", "remote-react-jobs",
        "remote-backend-jobs", "remote-frontend-jobs", "remote-full-stack-jobs",
        "remote-data-jobs", "remote-design-jobs", "remote-marketing-jobs",
        "remote-customer-support-jobs", "remote-sales-jobs", "remote-writing-jobs",
        "remote-non-tech-jobs", "remote-medical-jobs", "remote-teaching-jobs",
        "remote-legal-jobs", "remote-accounting-jobs", "remote-crypto-jobs"
    ]
    
    def __init__(self):
        self.jobs = []
        self.scraped_ids = set()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://remoteok.com/",
            "Accept": "application/json"
        }
        self.rp = RobotFileParser()
        self.rp.set_url(urljoin(self.BASE_URL, "robots.txt"))
        try:
            self.rp.read()
            logging.info("Successfully loaded robots.txt")
        except Exception as e:
            logging.error(f"Error reading robots.txt during init: {e}")

    def check_robots_compliance(self, url):
        try:
            can_fetch = self.rp.can_fetch(self.USER_AGENT, url)
            if not can_fetch:
                logging.warning(f"Robots.txt DISALLOWS scraping {url}")
            return can_fetch
        except:
            return False

    def scrape_category_json(self, category):
        """Fetches the JSON feed for a specific category."""
        # Clean category name to URL format
        if not category.endswith("json"):
            feed_url = f"{self.BASE_URL}/{category}.json"
        else:
            feed_url = f"{self.BASE_URL}/{category}"
            
        if not self.check_robots_compliance(feed_url):
            logging.warning(f"Skipping {feed_url} due to robots.txt")
            return

        logging.info(f"Fetching JSON Feed: {feed_url}")
        
        try:
            response = requests.get(feed_url, headers=self.headers, timeout=20)
            if response.status_code == 429:
                logging.error(f"Rate limited (429) on {category}. Waiting...")
                time.sleep(10)
                return
                
            response.raise_for_status()
            data = response.json()
            
            added_count = 0
            for job in data:
                # Validate job object
                if not isinstance(job, dict) or 'id' not in job: 
                    continue
                
                job_id = str(job.get('id'))
                if job_id in self.scraped_ids:
                    continue
                
                # Extract fields
                job_data = {
                    "Job ID": job_id,
                    "Job Title": job.get('position', job.get('title', 'N/A')),
                    "Company Name": job.get('company', 'N/A'),
                    "Job Tags": ", ".join(job.get('tags', [])) if isinstance(job.get('tags'), list) else "N/A",
                    "Location": job.get('location', 'Remote'),
                    "Job Type": "Full-time", # JSON feed standard
                    "Date Posted": job.get('date', 'N/A'),
                    "Job URL": job.get('url', 'N/A'),
                    "Category": category,
                    "Scraped Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                self.jobs.append(job_data)
                self.scraped_ids.add(job_id)
                added_count += 1
                
            logging.info(f"Extracted {added_count} new jobs from {category}. Total Unique: {len(self.jobs)}")
            
        except Exception as e:
            logging.error(f"Error fetching {category}: {e}")

    def run(self, target_jobs=600):
        logging.info(f"Starting Direct JSON Scraper. Target: {target_jobs} jobs.")
        
        random.shuffle(self.CATEGORIES) # Shuffle to vary requests
        
        for category in self.CATEGORIES:
            if len(self.jobs) >= target_jobs:
                logging.info(f"Target of {target_jobs} reached.")
                break
            
            self.scrape_category_json(category)
            
            # Smart delay
            delay = random.uniform(2.0, 4.0)
            logging.info(f"Sleeping {delay:.2f}s...")
            time.sleep(delay)
            
        self.save_raw_data()
        
    def save_raw_data(self):
        if not self.jobs:
            logging.warning("No jobs were scraped.")
            return
            
        df = pd.DataFrame(self.jobs)
        out_path = os.path.join("data", "raw", "remoteok_raw.csv")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        try:
            df.to_csv(out_path, index=False, encoding="utf-8-sig")
            logging.info(f"Saved {len(self.jobs)} jobs to {out_path}")
        except Exception as e:
            logging.error(f"Error saving data: {e}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    scraper = RemoteOKScraper()
    scraper.run(target_jobs=600)
