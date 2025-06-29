import requests
import logging
from bs4 import BeautifulSoup
from multiprocessing import Queue
from typing import List

@staticmethod
def _extract_company_symbols(page_html: str):
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
def _get_sp_500_companies(urls: List[str]):
    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            logging.error("wiki fail")
            return []
        
        yield from _extract_company_symbols(response.text)


@staticmethod
def run(urls: List[str], output_queues: list[Queue]):
    # can add workers here in order to run multiple urls in parallel
    count = 0
    for symbol in _get_sp_500_companies(urls):
        for out in output_queues:
            out.put(symbol)
        count += 1
        if count > 10:
            break

    # for out in output_queues:
    #     for _ in range(20):
    #         out.put('DONE')
