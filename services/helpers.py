import json
import os
import requests
import shutil
from urllib.parse import urlparse, urljoin

from google.oauth2 import service_account

def clear_images_folder(folder_path='images/'):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

def download_image(url, download_path='images/'):
    if not url.startswith(('http:', 'https:')):
        print(f"Skipping non-HTTP/HTTPS URL: {url}")
        return

    # Extract the file extension and check if it's in the allowed list
    filename = urlparse(url).path.split('/')[-1].split('?')[0]
    allowed_extensions = ['jpg', 'jpeg', 'png']
    extension = filename.split('.')[-1].lower()
    if extension not in allowed_extensions:
        return

    try:
        response = requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            filepath = os.path.join(download_path, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def download_images(image_urls, download_path='images/'):
    """Downloads all images from a list of image URLs."""
    # Ensure the folder exists
    os.makedirs(download_path, exist_ok=True)

    for url in image_urls:
        try:
            download_image(url, download_path)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

def load_credentials():
    credentials_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY")
    if credentials_path:
        try:
            with open(credentials_path, 'r') as credentials_file:
                credentials_json = credentials_file.read()
                credentials = service_account.Credentials.from_service_account_info(json.loads(credentials_json))
                return credentials
        except Exception as e:
            print(f"Failed to load credentials: {e}")
    else:
        print("GOOGLE_SERVICE_ACCOUNT_KEY environment variable is not set.")
    return None

def format_findings(moderation_list):
    if moderation_list:
        moderation_categories = "\n- ".join([f'"{category}"' for category in moderation_list])
        message = (f"The content has been flagged for containing references to the following categories:\n"
                   f"- {moderation_categories}.\n"
                   "These may not be suitable for children. Please review carefully. \n")
        return message