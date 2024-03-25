import argparse
from config import GCP_PROJECT_ID, SCRAPER_API_KEY
from services import helpers, nlp, scraper, vision

def main(url):
    if not GCP_PROJECT_ID or not SCRAPER_API_KEY:
        print("Please ensure GCP_PROJECT_ID and SCRAPER_API_KEY are set in config.py.")
        return

    # Fetch content (text and images) from URL.
    html_content = scraper.fetch_content(url, SCRAPER_API_KEY)

    if html_content:
        # Retrieve content (text and images) from URL.
        texts, resolved_image_urls = scraper.extract_content(html_content, url)
        combined_text = " ".join(texts)
        
        # Process text via NLP APIs to analyze for content moderation.
        print(f"Analyzing textual information in {url} ... \n")
        analysis_result = nlp.analyze_text(combined_text)
        if analysis_result:
            print(analysis_result)
        
        # Process images. Download locally to send for analysis. 
        print(f"Analyzing images in {url} ... \n")
        helpers.download_images(resolved_image_urls)
        
        # Connect to Vision API for analysis
        print(vision.analyze_images_in_folder())

        # Cleanup image folder after analysis.
        helpers.clear_images_folder()
    else:
        print("Failed to retrieve content.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze web content for moderation.")
    parser.add_argument("url", help="The URL of the website to analyze")
    
    args = parser.parse_args()
    main(args.url)
