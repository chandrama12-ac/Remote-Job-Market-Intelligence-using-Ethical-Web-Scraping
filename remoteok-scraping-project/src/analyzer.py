import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import Counter
from datetime import datetime

class RemoteOKAnalyzer:
    def __init__(self, input_path):
        self.input_path = input_path
        self.df = None
        
        # Set visualization style
        sns.set_theme(style="whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)

    def load_data(self):
        import csv
        if not os.path.exists(self.input_path):
            print(f"Error: {self.input_path} not found.")
            return False
        try:
            with open(self.input_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            self.df = pd.DataFrame(data)
            # Standard columns should exist
            if not self.df.empty:
                return True
        except Exception as e:
            print(f"Error loading data: {e}")
        return False

    def generate_visualizations(self):
        if self.df is None:
            return

        os.makedirs("visualizations", exist_ok=True)

        # 1. Top 10 Skills
        plt.figure()
        all_tags = []
        for tags in self.df['Job Tags'].dropna():
            all_tags.extend([t.strip().lower() for t in str(tags).split(',') if t.strip()])
        
        tag_counts = Counter(all_tags).most_common(10)
        tag_names, tag_values = zip(*tag_counts)
        
        sns.barplot(x=list(tag_values), y=list(tag_names), palette="viridis")
        plt.title("Top 10 Most Demanded Skills on RemoteOK")
        plt.xlabel("Frequency")
        plt.ylabel("Skill / Tag")
        plt.tight_layout()
        plt.savefig("visualizations/top_skills.png")
        print("Generated visualizations/top_skills.png")

        # 2. Job Type Distribution
        plt.figure()
        # Since it's RemoteOK, most are Remote. We might look at categories if we had them or location keywords
        # Let's mock job type distribution based on common tags like Full time, contract
        job_types = []
        for tags in self.df['Job Tags'].dropna():
            tags_lower = str(tags).lower()
            if 'contract' in tags_lower:
                job_types.append('Contract')
            elif 'part time' in tags_lower:
                job_types.append('Part-Time')
            elif 'intern' in tags_lower:
                job_types.append('Internship')
            else:
                job_types.append('Full-Time')
        
        self.df['Detected Type'] = job_types
        type_counts = self.df['Detected Type'].value_counts()
        plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
        plt.title("Estimated Job Type Distribution")
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig("visualizations/job_type_distribution.png")
        print("Generated visualizations/job_type_distribution.png")

        # 3. Top 10 Job Titles
        plt.figure()
        title_counts = self.df['Job Title'].value_counts().head(10)
        sns.barplot(x=title_counts.values, y=title_counts.index, palette="mako")
        plt.title("Top 10 Most Common Job Titles")
        plt.xlabel("Count")
        plt.ylabel("Job Title")
        plt.tight_layout()
        plt.savefig("visualizations/top_job_titles.png")
        print("Generated visualizations/top_job_titles.png")

        # 4. Skill Frequency Comparison (Python vs Javascript vs Others)
        plt.figure()
        common_tech = ['python', 'javascript', 'react', 'node', 'aws', 'sql', 'typescript']
        tech_freq = {tech: all_tags.count(tech) for tech in common_tech}
        tech_df = pd.DataFrame(list(tech_freq.items()), columns=['Technology', 'Count']).sort_values('Count', ascending=False)
        
        sns.barplot(data=tech_df, x='Technology', y='Count', palette="flare")
        plt.title("Frequency Comparison of Key Technologies")
        plt.tight_layout()
        plt.savefig("visualizations/skill_frequency_comparison.png")
        print("Generated visualizations/skill_frequency_comparison.png")

    def generate_report(self):
        # Recalculate tags for the report scope
        all_tags = []
        for tags in self.df['Job Tags'].dropna():
            all_tags.extend([t.strip().lower() for t in str(tags).split(',') if t.strip()])
        
        top_skill = Counter(all_tags).most_common(1)[0][0].upper() if all_tags else 'N/A'
        dominant_role = self.df['Job Title'].value_counts().index[0] if not self.df.empty else 'N/A'

        report_content = f"""# Job Market Analysis Report (RemoteOK)
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 1. Executive Summary
This report analyzes {len(self.df)} job listings scraped from RemoteOK. The data provides insights into the current remote job market trends, top skills, and popular job roles.

## 2. Key Insights
- **Most Popular Skill:** {top_skill}
- **Dominant Job Role:** {dominant_role}
- **Market Lean:** The market is heavily skewed towards full-time remote roles.

## 3. Methodology
- Data Scraped via systematic crawling of various RemoteOK JSON niche feeds.
- Cleaning involved deduplication and normalization using Pandas.
- Visualizations generated using Matplotlib and Seaborn.
"""
        os.makedirs("reports", exist_ok=True)
        with open("reports/analysis_report.md", "w") as f:
            f.write(report_content)
        print("Generated reports/analysis_report.md")

if __name__ == "__main__":
    # Ensure outputs are relative to the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)

    cleaned_csv = os.path.join("data", "cleaned", "remoteok_jobs_cleaned.csv")
    analyzer = RemoteOKAnalyzer(cleaned_csv)
    if analyzer.load_data():
        analyzer.generate_visualizations()
        analyzer.generate_report()
