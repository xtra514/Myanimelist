from time import sleep
from typing import Tuple

import requests
from bs4 import BeautifulSoup, Tag

from src.anime_details import AnimeDetails

ANIME_LIST_URL = "https://myanimelist.net/anime.php"


def get_html_table(html: str, attrs: dict | None = None, remove_header: bool = True) -> list[list[Tag]]:
    results: list[list[Tag]] = []
    bs = BeautifulSoup(html, features="html.parser")
    table = bs.find(name="table", attrs=attrs)
    if table and isinstance(table, Tag):
        rows = table.find_all(name="tr")
        for row in rows:
            if isinstance(row, Tag):
                columns = row.find_all("td")
                result: list[Tag] = []
                for column in columns:
                    if isinstance(column, Tag):
                        result.append(column)
                results.append(result)
    if remove_header and len(results) > 0:
        results.pop(0)
    return results


def download_anime_list(alpha_category: str, limit: int = 9999) -> list[Tuple]:
    results: list[Tuple] = []
    number_of_list = 50
    for index in range(limit):
        request_results = requests.get(url=ANIME_LIST_URL, params={"letter": alpha_category.upper(), "show": number_of_list * index}, timeout=9999)
        table = get_html_table(html=request_results.text, attrs={"border": 0, "cellpadding": 0, "cellspacing": 0})
        if len(table) > 0:
            for columns in table:
                if len(columns) > 1:
                    title_href = columns[1].find(name="a", attrs={"class": "hoverinfo_trigger fw-b fl-l"})
                    if title_href and isinstance(title_href, Tag):
                        results.append((title_href.string, title_href.attrs["href"]))
        else:
            break
    if len(results) == 0:
        return download_anime_list(alpha_category=alpha_category, limit=limit)
    return results


def download_anime_details(url: str) -> AnimeDetails:
    r = requests.get(url, timeout=9999)
    sleep(.1)
    return AnimeDetails(html=r.text)
