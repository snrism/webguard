# WebGuard: Content Moderation Tool

WebGuard is an open-source tool designed to help identify and moderate potentially unsafe web content, making the internet a safer place for everyone, especially children. Utilizing the power of Vision and Natural Language AI models, along with ScraperAPI for efficient web crawling, WebGuard analyzes web pages for adult content, violence, and other categories that may not be suitable for younger audiences.

## Features

- **Content Analysis**: Leverages Google Cloud's Natural Language API to analyze text for various moderation categories.
- **Image Safety Checks**: Uses Google Cloud's Vision API to detect unsafe content in images, supporting `.jpg` and `.png` formats.
- **Efficient Web Crawling**: Integrates with ScraperAPI to fetch and process web content, including dynamically loaded content via JavaScript.
- **Customizable Moderation**: Allows setting thresholds for different moderation categories to tailor content filtering according to specific needs.

<img width="1107" alt="image" src="https://github.com/snrism/webguard/assets/2106559/236a102e-ac17-41f7-b8c2-b3e873b23f27">

## Setup

### 1. Google Cloud Service Account Key

To access Google Cloud APIs, you'll need to set up a service account:

1. **Create a Service Account**: Visit the [Google Cloud Console](https://console.cloud.google.com/), navigate to "IAM & Admin" > "Service Accounts", and create a new service account.
2. **Grant Permissions**: Assign the service account the necessary roles (Service Usage Consumer) for accessing the Vision and Natural Language APIs.
3. **Generate a Key**: Create and download a JSON key for your service account.

**Environment Variable**:
Set the `GOOGLE_SERVICE_ACCOUNT_KEY` environment variable to the path of your downloaded JSON key file:

```bash
export GOOGLE_SERVICE_ACCOUNT_KEY="/path/to/your/service-account-file.json"
```

**Configuration**:
```
Open `config.py` and set your `GCP_PROJECT_ID` and `SCRAPER_API_KEY` with the appropriate values.
```

### 2. Scraper API Setup

ScraperAPI is used to crawl and fetch web content. To get started:

1. **Sign Up**: Create an account on [ScraperAPI](https://dashboard.scraperapi.com) and obtain your API key in your profile.
2. **Configuration**: Store your ScraperAPI key in a configuration file or as an environment variable for easy access within the tool.

### 3. Running the Tool.

To analyze a web page, run main.py with the URL as an argument:

```
python main.py <URL_to_analyze like https://example.com>
```

### 4. Image Downloads
Images found during web crawling are downloaded to the images/ folder for analysis by the Vision API. Before each run, the folder is cleared to ensure only current images are processed. Currently, only .jpg and .png images are supported.


### Contribution
Contributions to WebGuard are welcome! Whether it's adding new features, improving documentation, or reporting issues, your help makes WebGuard better for everyone.

### License
WebGuard is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

