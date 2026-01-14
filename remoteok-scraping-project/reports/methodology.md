# RemoteOK Scraper Methodology

## Data Collection
- **Sources**: RemoteOK.com (Public JSON Feeds).
- **Technique**: Systematic crawling of various category feeds (e.g., /api, /remote-dev-jobs.json) as the static HTML currently serves only placeholders. This approach maintains ethical compliance while satisfying the 500+ record target.
- **Ethics**: Honest User-Agents and implementation of request delays (1.5-3 seconds) as per robots.txt.

## Data Processing
- **Deduplication**: Used `pandas` to remove duplicate listings based on unique Job URLs.
- **Normalization**: Standardized date formats to ISO, cleaned whitespace from company names, and enforced Title Case for job titles.
- **Filtering**: Removed listings with critical missing data (i.e., no title or no company).

## Analysis
- **Keyword Extraction**: Split and flattened job tags to identify most frequent technical skills.
- **Role Analysis**: Statistical aggregation of job titles to identify hiring trends.
- **Visualization**: Leveraged `Seaborn` for high-quality data representation.

## Challenges
- **Infinite Scrolling**: Since the user requested no Selenium, we relied on deep-linking into specific category pages to access a larger pool of data than the homepage alone provides.
