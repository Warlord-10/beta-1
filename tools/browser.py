import os
import requests
from bs4 import BeautifulSoup




def open_browser(search_query):
    url = f"https://www.google.com/search?q={search_query}"
    os.system(f"start {url}")
    return "Browser opened"

def get_search_result(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, 'lxml')

    titles = soup.find_all("h3")
    results = {}
    for title in titles:
        link = title.find_parent("a")
        if link:
            results[title.text] = link["href"]

    print(results)
    return str(results)


if __name__ == "__main__":
    hindi_text = "यह एक परीक्षण है"  # This is a test
    print("यह एक परीक्षण है")
    query = input("Enter your search query: ")
    # query = "how to make pasta"
    results = get_search_result(query)

    if results:
        print(f"\nSearch Results: {len(results)} found")
        # print(results)
    else:
        print("No results found.")