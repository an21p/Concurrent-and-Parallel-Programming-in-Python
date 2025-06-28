import requests
import logging
from bs4 import BeautifulSoup

@staticmethod
def extract_company_symbols(page_html: str):
    soup = BeautifulSoup(page_html, "html.parser")
    table = soup.find(id="constituents")
    if table is None:
        logging.error("Could not find table with id 'constituents'")
        return
    table_rows = table.find_all("tr")
    for table_row in table_rows[1:]:
        symbol_cell = table_row.find('td')
        if symbol_cell:
            symbol = symbol_cell.text.strip('\n')
            yield symbol
    
@staticmethod
def get_sp_500_companies():
    response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    if response.status_code != 200:
        logging.error("wiki fail")
        return []
    
    yield from extract_company_symbols(response.text)
        
    
