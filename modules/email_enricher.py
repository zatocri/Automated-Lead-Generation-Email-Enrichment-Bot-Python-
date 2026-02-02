import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class EmailEnricher:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        self.ignore_list = ['sentry', 'wix', 'example', 'jpg', 'png', 'gif', 'bootstrap']

    def get_email(self, website_url):
        if not website_url: return None
        if not website_url.startswith('http'):
            website_url = 'http://' + website_url

        try:
            response = requests.get(website_url, headers=self.headers, timeout=10)
            emails = self._extract_emails(response.text)

            # If no email on home, check contact page
            if not emails:
                soup = BeautifulSoup(response.text, 'html.parser')
                contact_url = self._find_contact_link(soup, website_url)
                if contact_url:
                    resp_contact = requests.get(contact_url, headers=self.headers, timeout=10)
                    emails.update(self._extract_emails(resp_contact.text))

            return ", ".join(emails) if emails else "Not Found"
        except:
            return "Connection Error"

    def _extract_emails(self, text):
        found = set(re.findall(self.email_pattern, text))
        return {e.lower() for e in found if not any(j in e.lower() for j in self.ignore_list)}

    def _find_contact_link(self, soup, base_url):
        for a in soup.find_all('a', href=True):
            href = a['href'].lower()
            text = a.get_text().lower()
            if any(k in href or k in text for k in ['contact', 'contacto', 'about']):
                return urljoin(base_url, a['href'])
        return None