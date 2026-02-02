import os
import time
import pandas as pd
import re
import config
from modules.browser_engine import BrowserEngine
from modules.maps_parser import parse_business_list, parse_detail_view
from modules.email_enricher import EmailEnricher


def clean_data(leads):
    """
    Performs data cleaning and deduplication on the leads list.
    """
    if not leads:
        return pd.DataFrame()

    df = pd.DataFrame(leads)

    # 1. Basic string cleaning and placeholder removal
    placeholders = ["No Website", "Not Found", "Pending", "Error (Site Unreachable)"]
    df = df.replace(placeholders, None)

    # 2. Deduplication: Remove repetitions of places and websites
    # Deduplicate by maps_url (exact location)
    df.drop_duplicates(subset=['maps_url'], keep='first', inplace=True)

    # Deduplicate by name (prevents multiple branches of the same brand)
    df.drop_duplicates(subset=['name'], keep='first', inplace=True)

    # Deduplicate by website (prevents multiple leads for the same domain)
    # We only drop if a website exists (not null)
    df = df.sort_values('website', na_position='last')
    df.loc[df['website'].notna(), :] = df[df['website'].notna()].drop_duplicates(subset=['website'], keep='first')
    df.dropna(subset=['name'], inplace=True)  # Clean up any rows affected by subset drops

    # 3. Phone number normalization (digits only)
    if 'phone' in df.columns:
        df['phone_clean'] = df['phone'].apply(lambda x: re.sub(r'\D', '', str(x)) if pd.notna(x) else None)

    # 4. Final column selection
    columns = ['name', 'email', 'phone', 'phone_clean', 'website', 'rating', 'maps_url']
    final_cols = [c for c in columns if c in df.columns]

    return df[final_cols]


def main():
    if not os.path.exists(config.OUTPUT_FOLDER):
        os.makedirs(config.OUTPUT_FOLDER)

    bot = BrowserEngine(headless=False)
    enricher = EmailEnricher()

    try:
        print(f"Starting search for: {config.SEARCH_QUERY}")
        list_html = bot.get_maps_data(config.SEARCH_QUERY)
        leads = parse_business_list(list_html)

        if len(leads) > config.MAX_RESULTS:
            leads = leads[:config.MAX_RESULTS]

        print(f"Processing {len(leads)} leads...")

        for i, lead in enumerate(leads):
            url = lead.get('maps_url')
            if not url:
                continue

            detail_html = bot.visit_business_page(url)
            details = parse_detail_view(detail_html)
            lead.update(details)

            website = lead.get('website')
            if website:
                email = enricher.get_email(website)
                lead['email'] = email if email else "Not Found"
            else:
                lead['email'] = "No Website"

            time.sleep(config.SCROLL_PAUSE_TIME)

        # Apply cleaning and deduplication logic
        df_cleaned = clean_data(leads)

        df_cleaned.to_csv(config.OUTPUT_PATH, index=False)
        print(f"Cleaned data saved to: {config.OUTPUT_PATH}")

    except Exception as e:
        print(f"Error in main execution: {e}")
    finally:
        bot.driver.quit()


if __name__ == "__main__":
    main()