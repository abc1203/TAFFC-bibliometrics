import json
import pandas as pd
from collections import Counter

def calculate_frequency_by_issue(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Extract records from the JSON data
    records = []
    for entry in data:
        year = entry.get("Year", "")
        issue = entry.get("Issue #", "")
        keywords = entry.get("IEEE Keywords", [])
        records.append((year, issue, keywords))
    
    # Count the frequency of each keyword
    keyword_counter = Counter()
    issue_keyword_count = Counter()
    
    for year, issue, keywords in records:
        issue_keyword_count[(year, issue)] += len(keywords)
        for keyword in keywords:
            keyword_counter[(year, issue, keyword)] += 1
    
    # Convert the counter to a list of dictionaries with ratio
    frequency_data = []
    for (year, issue, keyword), frequency in keyword_counter.items():
        total_keywords_in_issue = issue_keyword_count[(year, issue)]
        ratio = (frequency / total_keywords_in_issue) * 100
        ratio = round(ratio, 4)
        frequency_data.append({
            "Year": year,
            "Issue": issue,
            "Keyword": keyword,
            "Frequency": frequency,
            "Ratio": ratio
        })
    
    return frequency_data



# calculate by year
def calculate_frequency_by_year(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Extract records from the JSON data
    records = []
    for entry in data:
        year = entry.get("Year", "")
        if year <= 2023:
            keywords = entry.get("IEEE Keywords", [])
            records.append((year, keywords))
    
    # Count the frequency of each keyword
    keyword_counter = Counter()
    year_keyword_count = Counter()
    
    for year, keywords in records:
        year_keyword_count[year] += len(keywords)
        for keyword in keywords:
            keyword_counter[(year, keyword)] += 1
    
    # Convert the counter to a list of dictionaries with ratio
    frequency_data = []
    for (year, keyword), frequency in keyword_counter.items():
        total_keywords_in_year = year_keyword_count[year]
        ratio = (frequency / total_keywords_in_year) * 100
        ratio = round(ratio, 4)
        frequency_data.append({
            "Year": year,
            "Keyword": keyword,
            "Frequency": frequency,
            "Ratio": ratio
        })
    
    return frequency_data


def save_to_csv(frequency_data, output_csv_file):
    df = pd.DataFrame(frequency_data)
    df.to_csv(output_csv_file, index=False)



if __name__ == "__main__":
    json_file = 'data/TAFFC_IEEEkeywords.json'
    output_csv_file_issue = 'data/TAFFC_keywords_by_issue.csv'
    output_csv_file_year = 'data/TAFFC_keywords_by_year.csv'

    frequency_data_issue = calculate_frequency_by_issue(json_file)
    frequency_data_year = calculate_frequency_by_year(json_file)
    save_to_csv(frequency_data_issue, output_csv_file_issue)
    save_to_csv(frequency_data_year, output_csv_file_year)

    print("Keyword frequency data has been saved")
