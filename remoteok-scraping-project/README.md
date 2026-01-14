# RemoteOK Scraping Project

A production-ready Python project that ethically scrapes job listings from RemoteOK, cleans the data, and generates market trend visualizations and reports.

## Project Structure
```text
remoteok-scraping-project/
│
├── README.md               # Project documentation
├── requirements.txt         # Project dependencies
│
├── src/                    # Source code
│   ├── scraper.py           # Ethical scraping logic
│   ├── data_cleaner.py      # Cleaning & preprocessing
│   └── analyzer.py          # Analysis & visualization
│
├── data/                   # Data storage
│   ├── raw/                # Unprocessed scraped data
│   │   └── remoteok_raw.csv
│   └── cleaned/            # Normalized dataset
│       └── remoteok_jobs_cleaned.csv
│
├── visualizations/          # Generated charts (PNG)
│   ├── top_skills.png
│   ├── job_type_distribution.png
│   ├── top_job_titles.png
│   └── skill_frequency_comparison.png
│
├── reports/                 # Analysis documentation
│   ├── analysis_report.md   # Executive summary report
│   └── methodology.md       # Technical scraping methodology
```

## Setup & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Execution Order
To process the data from scratch, run the scripts in the following order from the project root:

1. **Scrape Data**:
   ```bash
   python src/scraper.py
   ```
2. **Clean Data**:
   ```bash
   python src/data_cleaner.py
   ```
3. **Analyze Data**:
   ```bash
   python src/analyzer.py
   ```

## Ethical Compliance
This project strictly follows ethical scraping guidelines:
- **robots.txt**: Automatically verified before every request.
- **Rate-Limiting**: Mandatory random delays (3.0s - 5.0s) for politeness.
- **Public Data**: Only targets official public feeds intentionally served by the site.
