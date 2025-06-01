import os
import requests
import bs4
import json


def fetch_page(url):
    """Fetches the HTML of the URL"""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status() # Ensure the request was successful
        return r.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def parse_wikitable(html):
    """Parses the wikitable"""
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    return table if table else None


def parse_table_headers(table):
    """Parses the table headers"""
    headers = table.find_all('th')
    return [header.text.strip() for header in headers] if headers else []


def parse_rows(table):
    """Parses the table rows"""
    rows = table.find_all('tr')
    return rows[1:] if rows else []


def parse_columns(row):
    """Parses the table columns"""
    cols = row.find_all('td')
    return [col.text.strip() for col in cols] if cols else []


def parse_cells(columns):
    """Parses the table cells"""
    links = []
    for col in columns :
        links.extend(col.find_all('a'))
    return links


def scrape(url):
    """Scrapes the URL"""
    html = fetch_page(url)
    if not html:
        return {'error': 'Page could not be fetched'}

    table = parse_wikitable(html)
    if not table:
        return {'error': 'Wikie table was not found'}

    headers = parse_table_headers(table)
    rows = parse_rows(table)

    data = []
    for row in rows:
        row_data = parse_columns(row)
        if row_data:
            data.append(row_data)

    file_path = os.path.join(os.getcwd(), 'data.json')
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({'headers': headers, 'data': data}, f, indent=4)
        return {'Succeeded': 'Data written to file', 'file_path': file_path}
    except OSError as e:
        print(f"Could not write to file: {e}")
        return {'error': f'File could not be written to file: {e}'}
