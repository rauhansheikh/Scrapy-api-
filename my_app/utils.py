import requests
from .models import SearchQuery, SearchResult

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
