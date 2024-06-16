from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import json


# get past years of TAFFC issues
def get_all_years():
    year_elements = driver.find_elements(By.CSS_SELECTOR, 'div.issue-details-past-tabs.year ul li a')
    years = [elem.text for elem in year_elements]
    return years


# obtain all issues url from all past issues of TAFFC
def get_issue_urls_for_year(base_url, year):
    driver.get(base_url)
    time.sleep(2)
    year_tab = driver.find_element(By.XPATH, f"//a[text()='{year}']")
    if year != 2024: year_tab.click()
    time.sleep(2)  # Wait for the dynamic content to load
    issue_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="tocresult.jsp?isnumber="][href*="&punumber="]')
    issues = [(elem.text.strip(), elem.get_attribute('href')) for elem in issue_elements]
    return issues


# obtain all paper urls from the issue
def get_paper_urls(issue_url):
    driver.get(issue_url)
    time.sleep(2)  # Wait for the dynamic content to load
    paper_urls = set()

    # Determine total number of pages
    pagination_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[class^="stats-Pagination_"]')
    total_pages = max([int(btn.text) for btn in pagination_buttons if re.match(r'^stats-Pagination_\d+$', btn.get_attribute('class'))]) if pagination_buttons else 1

    for page in range(1, total_pages + 1):
        if page > 1:
            # Click on the page number button to navigate to the next page
            page_button = driver.find_element(By.XPATH, f"//button[text()='{page}']")
            page_button.click()
            time.sleep(2)  # Wait for the next page to load
        
        paper_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/document/"]')
        for elem in paper_elements:
            href = elem.get_attribute('href')
            if re.match(r'^https://ieeexplore.ieee.org/document/\d+/$', href):
                paper_urls.add(href)

    return paper_urls


# extract the IEEE keywords & title from a paper URL
def extract_IEEEkeywords_and_title(paper_url):
    driver.get(paper_url)
    time.sleep(1.5)  # Wait for the dynamic content to load
    
    try:
        # extract title
        title_element = driver.find_element(By.CSS_SELECTOR, 'h1.document-title span')
        title = title_element.text.strip()

        # extract IEEE keywords
        keyword_header = driver.find_element(By.CSS_SELECTOR, 'div.accordion-header[id="keywords-header"]')
        keyword_header.click()
        time.sleep(1.5)

        keywords_elements = driver.find_elements(By.CSS_SELECTOR, 'a.stats-keywords-list-item')
        ieee_keywords = set()
        for elem in keywords_elements:
            data_tealium_data = elem.get_attribute('data-tealium_data')
            if data_tealium_data:
                keyword_info = json.loads(data_tealium_data)
                if keyword_info.get('keywordType') == 'IEEE Keywords' and elem.text.strip() != '':
                    ieee_keywords.add(elem.text.strip())
        
        return title, list(ieee_keywords)
    except Exception:
        return title, []



def main():
    base_url = 'https://ieeexplore.ieee.org/xpl/issues?punumber=5165369&isnumber=10542474'

    years = get_all_years()
    all_data = []

    for year in years:
        year = int(year)
        issues = get_issue_urls_for_year(base_url, year)

        for issue_text, issue_url in issues:
            issue_number = re.search(r'Issue (\d+)', issue_text).group(1)
            paper_urls = get_paper_urls(issue_url)

            for paper_url in paper_urls:
                title, keywords = extract_IEEEkeywords_and_title(paper_url)
                all_data.append({
                    "Year": year,
                    "Issue #": issue_number,
                    "Title": title,
                    "IEEE Keywords": keywords
                })
                print("Year: {}, Issue #: {}, Title: '{}', IEEE Keywords: {}".format(year, issue_number, title, keywords))

    # Convert to JSON string and save to file
    json_data = json.dumps(all_data, indent=4)
    with open('taffc_IEEEkeywords.json', 'w') as json_file:
        json_file.write(json_data)


if __name__ == "__main__":
    # Setup Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        main()
    finally:
        driver.quit()
