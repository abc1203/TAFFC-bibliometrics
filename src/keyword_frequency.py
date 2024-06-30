import json
import pandas as pd
from collections import Counter

def calculate_keyword_frequency(json_file):
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
    for year, issue, keywords in records:
        for keyword in keywords:
            keyword_counter[(year, issue, keyword)] += 1
    
    # Convert the counter to a list of dictionaries
    frequency_data = [
        {"Year": year, "Issue": issue, "Keyword": keyword, "Frequency": frequency}
        for (year, issue, keyword), frequency in keyword_counter.items()
    ]
    
    return frequency_data

def save_to_csv(frequency_data, output_csv_file):
    df = pd.DataFrame(frequency_data)
    df.to_csv(output_csv_file, index=False)

if __name__ == "__main__":
    json_file = 'data/TAFFC_IEEEkeywords.json'
    output_csv_file = 'data/TAFFC_keyword_frequency.csv'

    frequency_data = calculate_keyword_frequency(json_file)
    save_to_csv(frequency_data, output_csv_file)

    print("Keyword frequency data has been saved to", output_csv_file)
