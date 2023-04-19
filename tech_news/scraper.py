import requests
from time import sleep
from bs4 import BeautifulSoup
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    header_site = {"user-agent": "Fake user-agent"}
    sleep(1)
    try:
        response = requests.get(url, headers=header_site, timeout=3)
        response.raise_for_status()
    except (requests.HTTPError, requests.ReadTimeout):
        return None
    else:
        return response.text


# Requisito 2
def scrape_updates(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    result = []
    for line in soup.find_all('a', attrs={'class': 'cs-overlay-link'}):
        result.append(line['href'])
    return result


# Requisito 3
def scrape_next_page_link(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    try:
        result = soup.find('a', attrs={'class': 'next'}).get('href')
    except AttributeError:
        return None
    else:
        return result


# Requisito 4
def scrape_news(html_content):
    timestamp = 0
    soup = BeautifulSoup(html_content, "html.parser")
    url = soup.find("link", rel="canonical").get("href")
    title = soup.h1.get_text().strip()
    timestamp = soup.find("li", {"class": "meta-date"}).text
    writer = soup.find("a", {"class": ["url", "fn", "n"]}).get_text().strip()
    reading_time = (soup.find("li", {"class": "meta-reading-time"}).text)[:2]
    int_reading_time = int(reading_time)
    summary = soup.find("p").get_text().strip()
    category = soup.find("span", {"class": "label"}).get_text().strip()

    data_news = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": int_reading_time,
        "summary": summary,
        "category": category,
    }

    return data_news


# Requisito 5
def get_tech_news(amount):
    blog = fetch('https://blog.betrybe.com/')

    info_news = []
    while len(info_news) < amount:
        info_news.extend(scrape_updates(blog))
        blog = fetch(scrape_next_page_link(blog))
    scraped_infos = []
    for link in info_news[:amount]:
        blog = fetch(link)
        scraped_infos.append(scrape_news(blog))
    create_news(scraped_infos)
    return scraped_infos


if __name__ == '__main__':
    content = fetch('https://blog.betrybe.com/')
    print(get_tech_news(10))
