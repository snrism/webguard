import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import base64
import os

def fetch_content(url, api_key):
    """Fetches webpage content using ScraperAPI."""
    params = {'api_key': api_key, 'url': url}
    response = requests.get('http://api.scraperapi.com', params=params)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch content. Status Code: {response.status_code}")
        return None

def resolve_urls(base_url, relative_urls):
    """Resolves relative URLs to absolute URLs based on a base URL."""
    return [urljoin(base_url, rel_url) for rel_url in relative_urls]

def extract_content(html_content, base_url):
    """Extracts and prints text and images from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    texts = list(soup.stripped_strings)
    images = [img['src'] if img.has_attr('src') else img['data-src'] for img in soup.find_all('img') if img.has_attr('src') or img.has_attr('data-src')]
    return texts, resolve_urls(base_url, images)
