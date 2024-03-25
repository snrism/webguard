# Your Google Cloud Project ID for billing purposes.
# Replace the empty string with <Your_GCP_Project_ID>.
GCP_PROJECT_ID = ""

# Scraper API key for crawling content.
# Obtain your key from https://docs.scraperapi.com/v/python and replace the empty string below.
SCRAPER_API_KEY = ""

# Content Moderation thresholds. 
# Checkout the categories here: https://cloud.google.com/natural-language/docs/moderating-text
# Feel free to adjust the thresholds as per your requirement.
CONTENT_MODERATION_THRESHOLDS = {
    "Toxic": 0.5, 
    "Derogatory": 0.5, 
    "Sexual": 0.5, 
    "Violent": 0.5, 
    "Insult": 0.8,
    "Profanity": 0.8,
    "Death, Harm & Tragedy": 0.3,
    "Firearms & Weapons": 0.3,
    "Illicit Drugs": 0.3,
    "War & Conflict": 0.3
}