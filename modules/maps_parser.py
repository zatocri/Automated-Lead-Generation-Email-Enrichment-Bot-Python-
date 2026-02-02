from bs4 import BeautifulSoup


def parse_business_list(html_source):
    results = []
    seen_urls = set()
    if not html_source: return results

    soup = BeautifulSoup(html_source, 'html.parser')
    for card in soup.select("div[role='feed'] > div"):
        try:
            link_el = card.find("a", class_="hfpxzc")
            if not link_el: continue

            url = link_el.get('href')
            if url in seen_urls: continue

            seen_urls.add(url)
            name_el = card.find("div", class_="fontHeadlineSmall")
            rating_el = card.find("span", class_="MW4etd")

            results.append({
                'name': name_el.get_text(strip=True) if name_el else "Unknown",
                'maps_url': url,
                'rating': rating_el.get_text(strip=True) if rating_el else "N/A",
                'website': None,
                'phone': None
            })
        except:
            continue
    return results


def parse_detail_view(html_source):
    details = {'website': None, 'phone': None}
    if not html_source: return details

    soup = BeautifulSoup(html_source, 'html.parser')
    try:
        # Extract website link
        site = soup.find("a", {"data-item-id": "authority"})
        if site: details['website'] = site.get('href')

        # Extract phone number
        phone_btn = soup.select_one("button[data-item-id^='phone:tel:']")
        if phone_btn:
            phone_div = phone_btn.find("div", class_="Io6YTe")
            if phone_div: details['phone'] = phone_div.get_text(strip=True)
    except:
        pass
    return details