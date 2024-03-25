import json
import logging
from typing import Optional
import os

from google.cloud import language_v2
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import GoogleAPICallError, RetryError

from config import CONTENT_MODERATION_THRESHOLDS, GCP_PROJECT_ID
from .helpers import load_credentials, format_findings

def process_responses(moderation_response) -> str:
    """
    Processes the responses from moderation analysis.

    Args:
      moderation_response: The response from classify_text.

    Returns:
      A string containing moderation response details.
    """
    moderation_list = []
    for moderation in moderation_response.moderation_categories:
        if moderation.name in CONTENT_MODERATION_THRESHOLDS:
            # print(f"{moderation.name}: {moderation.confidence}")
            if moderation.confidence > CONTENT_MODERATION_THRESHOLDS[moderation.name]:
                moderation_list.append(f"{moderation.name}")
    if moderation_list:
        return format_findings(moderation_list)
    else:
        return "All analyzed text appears to be suitable for children."

def analyze_text(text: str) -> Optional[str]:
    """
    Analyzes the text and checks for moderation categories.

    Args:
      text: The text content to analyze.

    Returns:
      A message indicating if the input text contains NSFW content or unsupported Entity names,
      or None if no issues are found.
    """
    client_options = ClientOptions(quota_project_id=GCP_PROJECT_ID)
    try:
        credentials = load_credentials()
    except Exception as e:
        return "Sorry, unable to load Google Service account credentials."
    
    try:
        client = language_v2.LanguageServiceClient(client_options=client_options, credentials=credentials)
    except GoogleAPICallError as e:
        logging.error(f"Unable to connect to LanguageService Client: {e}")
        return "Sorry, unable to connect Google's LanguageService."

    document = language_v2.Document(
        content=text,
        type_=language_v2.Document.Type.PLAIN_TEXT,
        language_code="en"
    )

    try:
        moderation_response = client.moderate_text(request={"document": document})
    except (GoogleAPICallError, RetryError) as e:
        logging.error(f"Unable to provess to LanguageService Client response: {e}")
        return "Sorry, unable to process moderation API response"

    moderation_issue_detected = process_responses(moderation_response)

    if moderation_issue_detected:
        return moderation_issue_detected
    return None