import requests
from .models import SearchQuery, SearchResult
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def perform_search_and_save(query):
    headers = {
        "X-API-KEY": "a1f790320f4a58b62d112c128e2de66859054a1b", 
        "Content-Type": "application/json"
    }
    json_data = {
        "q": query
    }

    response = requests.post("https://google.serper.dev/search", headers=headers, json=json_data)
    data = response.json()

    print(data)  

    search_entry = SearchQuery.objects.create(query=query)

    for result in data.get("organic", []):
        SearchResult.objects.create(
            query=search_entry,
            title=result.get("title", ""),
            link=result.get("link", ""),
            snippet=result.get("snippet", ""),
        )

    return search_entry


def scrape_page_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(2) 

    page_title = driver.title
    body_text = driver.find_element(By.TAG_NAME, "body").text

    driver.quit()

    return {
        "title": page_title,
        "content": body_text[:500]  
    }
