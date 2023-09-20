import requests
from bs4 import BeautifulSoup
import params


def scrape_news_headlines(url, category):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = []
        headline_elements = soup.find_all("a")
    
        for headline in headline_elements:
            text = headline.get_text(strip=True)
            link = headline.get("href")
            if text and link:
                if filter_sort(text, headlines):
                    link = absolute_url(link, url)
                    headlines.append((text, link, category))
        
        return headlines

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def scrape_multiple_urls(urls):
    all_headlines = []
    for category, url_list in urls.items():
        category_headlines = []
        for url in url_list:
            headlines = scrape_news_headlines(url, category)
            # limit 2 per URL
            category_headlines.extend(headlines[:2])
            # limit 5 per category
            if len(category_headlines) >= 5:
                break  
        all_headlines.extend(category_headlines[:5])

    return remove_duplicates(all_headlines)


# rejects articles unrelated to interests
def filter_sort(headline, list):
    headline_low = headline.lower()
    if headline not in list:
        for interest in params.interests:
            if interest.lower() in headline_low:
                return True
    return False


# returns follow link from short href
def absolute_url(link, url):
    if "https" not in link:
        parts = url.split("/")
        base_url = parts[0] + "//" + parts[2]
        return base_url + link
    else:
        return link


def remove_duplicates(headlines):
    unique_list = []

    for item in headlines:
        if item not in unique_list:
            unique_list.append(item)

    # remove one worded headlines 
    filtered_list = [
        article for article in unique_list 
        if len(article[0].split()) > 1
        and article[0] != "Premier League"
    ]

    return filtered_list