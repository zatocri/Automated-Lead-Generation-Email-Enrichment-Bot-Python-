Google Maps Lead Extractor & Email Finder

A modular Python-based web scraping solution designed to extract business data from Google Maps and perform deep contact enrichment by crawling business websites for email addresses.
Key Features

    Automated Data Extraction: Handles dynamic content and infinite scrolling on Google Maps using Selenium.

    Deep Email Enrichment: Automatically visits discovered business websites to find contact emails.

    Intelligent Filtering: Filters out non-functional email captures like image paths (.svg, .png) and generic placeholders.

    Data Integrity: Performs multi-layer deduplication based on unique Google Maps URLs and website domains.

    CRM-Ready Output: Exports cleaned data to CSV with normalized phone numbers.

Technical Stack

    Language: Python

    Automation: Selenium WebDriver

    Parsing: BeautifulSoup4

    Data Management: Pandas

    Driver Management: Webdriver-manager 

Project Structure

    ├── main.py                # Application entry point and workflow logic
    ├── config.py              # Centralized search and system settings
    ├── modules/
    ├── browser_engine.py  # Selenium driver setup and navigation
    ├── maps_parser.py     # HTML parsing for business lists and details
    └── email_enricher.py  # Website crawling and email regex extraction
    ├── requirements.txt       # Project dependencies 
    └── output/                # Generated CSV lead lists

Setup and Installation

    Clone the repository:
    Bash

    git clone https://github.com/your-username/google-maps-scraper.git
    cd google-maps-scraper

    Install dependencies:
    Bash

    pip install -r requirements.txt

    Configure your search: Open config.py and modify the SEARCH_QUERY and MAX_RESULTS variables.

    Run the scraper:
    Bash

    python main.py

Solution Overview

This tool was built to solve the challenge of manual lead generation.
By automating the extraction and enrichment process, it provides businesses with high-intent, live data directly from the source. 
The system is designed with a modular architecture, making it easy to adapt for different industries or additional data points (like social media links) in the future.