from bs4 import BeautifulSoup
import requests

# News site URL info
BASE_URL = "https://psmag.com/"
AUTHOR_URL = BASE_URL + "author/nick-hagar-1"

def collect_urls(author_page):
    """Scrape author page for article links

    Args:
        author_page (str): URL for author page
    """
    r = requests.get(author_page)
    page_html = r.text
    soup = BeautifulSoup(page_html, features="lxml")
    link_elements = soup.find_all("phoenix-super-link")
    links = [BASE_URL + i["href"] for i in link_elements]
    return links

def send_to_wayback(links):
    """Archive stories via Wayback Machine

    Args:
        links (list): List of URLs to archive
    """
    for i in links:
        save_url = f"https://web.archive.org/save/{i}"
        response = requests.get(save_url)
            
        if response.status_code == 200:
            result = response.url
            # We're just printing the archive URLs, but we could save them too!
            print(f"✔ {result}")
        else:
            print(f"❌ Connection error for {i}")

def main():
    print("💻 Starting link collection")
    # Grab story links from author page
    links = collect_urls(AUTHOR_URL)
    print(f"✅ {len(links)} stories collected")
    print("📂 Archiving most recent 10")
    # Limit to most recent 10
    recent_links = links[:10]
    print("🔗 Archive links:")
    # Send to Wayback Machine
    send_to_wayback(recent_links)
    print("🎉 Success!")

if __name__ == "__main__":
    main()