import requests
from bs4 import BeautifulSoup
import json
import time  # Make sure to import the time module

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to scrape data from a single page
def scrape_page(page_number):
    url = f'https://anidb.net/anime/?h=1&noalias=1&orderby.name=0.1&page={page_number}&view=list'
    print(f"Accessing {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    anime_list = soup.select('table.animelist tbody tr')
    page_data = []
    for anime in anime_list:
        try:
            title = anime.select_one('td[data-label="Title"]').text.strip()
            rating = anime.select_one('td[data-label="Rating"]').text.strip()
            aired = anime.select_one('td[data-label="Aired"]').text.strip()

            # Exclude anime with a rating of "N/A"
            if rating != "N/A":
                anime_data = {'Title': title, 'Rating': rating, 'Aired': aired}
                page_data.append(anime_data)
                print(f"Anime scraped: {anime_data}")
            else:
                print(f"Anime excluded due to N/A rating: {title}")

        except AttributeError as e:
            print(f"Failed to scrape some data for page {page_number}, skipping this anime: {e}")

    return page_data

# Main scraping logic...
all_anime_data = []
total_pages = 436  # Total number of pages to scrape

for page_number in range(total_pages):
    page_data = scrape_page(page_number)
    all_anime_data.extend(page_data)
    time.sleep(1)  # Sleep for 1 second between requests to avoid being blocked by the server

# Save the data to a JSON file
json_filename = 'anime_data.json'
with open(json_filename, 'w', encoding='utf-8') as json_file:
    json.dump(all_anime_data, json_file, ensure_ascii=False, indent=4)

print(f"Data saved to {json_filename}")
