import json
import logging
from typing import Optional
import os

from google.cloud import vision
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import GoogleAPICallError, RetryError

from config import GCP_PROJECT_ID
from .helpers import load_credentials

def analyze_images_in_url(image_urls) -> str:
    """
    Detects unsafe content in the image.
    """
    client_options = ClientOptions(quota_project_id=GCP_PROJECT_ID)
    try:
        credentials = load_credentials()
    except Exception as e:
        return "Sorry, unable to load Google Service account credentials."

    try:
        client = vision.ImageAnnotatorClient(client_options=client_options, credentials=credentials)
    except GoogleAPICallError as e:
        print(f"Vision API client initialization failed: {e}")
        return "Sorry, unable to connect to ImageAnnotator Service."

    findings = []
    for url in image_urls:
        image = vision.Image(source=vision.ImageSource(image_uri=url))
        try:
            response = client.safe_search_detection(image=image)
            if response.error.message:
                print(f"Safe search detection failed for {url}: {response.error.message}")
                continue
        except (GoogleAPICallError, RetryError) as e:
            logging.error(f"Error during safe search detection for {url}: {e}")
            continue

        safe = response.safe_search_annotation
        # Checking for adult or violent content
        if any(level in (vision.Likelihood.LIKELY, vision.Likelihood.VERY_LIKELY) for level in (safe.adult, safe.violence)):
            findings.append(f"Image at {url} might contain content that is not suitable for children.")

    if findings:
        return " ".join(findings)
    else:
        return "All analyzed images appear to be suitable for children."

def analyze_images_in_folder(folder_path='images/'):
    """
    Detects unsafe content in the image.
    """

    files = os.listdir(folder_path)
    if not files:
        return ""

    client_options = ClientOptions(quota_project_id=GCP_PROJECT_ID)

    try:
        credentials = load_credentials()
    except Exception as e:
        return "Sorry, unable to load Google Service account credentials."

    try:
        client = vision.ImageAnnotatorClient(client_options=client_options, credentials=credentials)
    except GoogleAPICallError as e:
        print(f"Vision API client initialization failed: {e}")
        return "Sorry, unable to connect to ImageAnnotator Service."
    
    findings = []
    for filename in files:
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        response = client.safe_search_detection(image=image)
        safe = response.safe_search_annotation

        # Check each type of content individually
        if safe.adult in (vision.Likelihood.LIKELY, vision.Likelihood.VERY_LIKELY) and "ADULT" not in findings:
            findings.append("ADULT")
        if safe.violence in (vision.Likelihood.LIKELY, vision.Likelihood.VERY_LIKELY) and "VIOLENT" not in findings:
            findings.append("VIOLENT")
        if safe.racy in (vision.Likelihood.LIKELY, vision.Likelihood.VERY_LIKELY) and "RACY" not in findings:
            findings.append("RACY")
        
    # If any unsafe content was detected, append a detailed message to results
    if findings:
        content_types = ", ".join(findings)
        message = f"Input URL might contain {content_types} images that is not suitable for children."
        return message
    return "All analyzed images appear to be suitable for children."
