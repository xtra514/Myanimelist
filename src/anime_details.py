from dataclasses import dataclass, fields

import pydash
from bs4 import BeautifulSoup, Tag


@dataclass
class AnimeDetails:
    bs: BeautifulSoup
    title: str = '-'
    english_title: str = '-'
    type: str = '-'
    episodes: str | int = 0
    score: float | int = 0
    ranked: float | int = 0
    popularity: float | int = 0
    members: float | int = 0
    favorites: float | int = 0
    rating: str = '-'
    status: str = '-'
    aired: str = '-'
    premiered: str = '-'
    broadcast: str = '-'
    producers: str = '-'
    licensors: str = '-'
    studios: str = '-'
    source: str = '-'
    demographic: str = '-'
    duration: str = '-'
    genre: str = '-'
    theme: str = '-'
    genres: str = '-'
    themes: str = '-'
    demographics: str = '-'
    parent_story: str = '-'
    prequel: str = '-'
    side_story: str = '-'
    other: str = '-'
    sequel: str = '-'
    alternative_setting: str = '-'
    character: str = '-'
    summary: str = '-'
    alternative_version: str = '-'
    spin_off: str = '-'
    full_story: str = '-'
    synopsis: str = '-'

    def __init__(self, html: str) -> None:
        self.bs = BeautifulSoup(html, features="html.parser")
        self.set_details()

    def __str__(self) -> str:
        return "|".join([str(getattr(self, field.name)) for field in fields(self) if field.name != "bs"])

    def __iter__(self):
        for field in fields(self):
            if field.name != "bs":
                yield getattr(self, field.name)

    def set_details(self) -> None:
        self.title = self.get_tag_text(tag_name="h1", attrs={"class": "title-name h1_bold_none"})
        self.english_title = self.get_tag_text(tag_name="p", attrs={"class": "title-english title-inherit"})
        self.ranked = self.to_number(self.get_tag_text(tag_name="span", attrs={"class": "numbers ranked"}))
        self.popularity = self.to_number(self.get_tag_text(tag_name="span", attrs={"class": "numbers popularity"}))
        self.members = self.to_number(self.get_tag_text(tag_name="span", attrs={"class": "numbers members"}))
        self.score = self.to_number(self.get_tag_text(tag_name="div", attrs={"class": "fl-l score"}))
        self.synopsis = self.get_tag_text(tag_name="p", attrs={"itemprop": "description"})
        self.set_html_details()
        self.set_related_anime()
        self.format_details()

    def format_details(self) -> None:
        for field in fields(self):
            if isinstance(getattr(self, field.name), list):
                setattr(self, field.name, self.convert_arr_to_str(getattr(self, field.name)))

    def set_related_anime(self) -> None:
        table = self.get_table(attrs={"class": "anime_detail_related_anime"})
        for column in table:
            if len(column) == 2:
                if hasattr(self, pydash.snake_case(column[0].text.replace(":", ""))):
                    setattr(self, pydash.snake_case(column[0].text.replace(":", "")), column[1].text)
            elif len(column) == 4:
                if hasattr(self, pydash.snake_case(column[0].text.replace(":", ""))):
                    setattr(self, pydash.snake_case(column[0].text.replace(":", "")), column[1].text)
                if hasattr(self, pydash.snake_case(column[2].text.replace(":", ""))):
                    setattr(self, pydash.snake_case(column[2].text.replace(":", "")), column[3].text)

    def set_html_details(self) -> None:
        details = self.get_html_details()
        for detail in details:
            if ":" in detail[0]:
                key = pydash.snake_case(str(detail[0]).replace(":", ""))
                if key not in ["title", "ranked", "popularity", "members", "score", "synopsis"]:
                    if len(detail) == 2:
                        if hasattr(self, key) and (getattr(self, key) == "-" or getattr(self, key) == 0):
                            setattr(self, key, detail[1])
                    else:
                        if hasattr(self, key) and (getattr(self, key) == "-" or getattr(self, key) == 0):
                            setattr(self, key, detail[1:])

    def get_html_details(self) -> list[list[str]]:
        results: list[list[str]] = []
        divs = self.bs.find_all(name="div", attrs={"class": "spaceit_pad"})
        for div in divs:
            if isinstance(div, Tag) and ":" in div.text:
                result: list[str] = []
                for content in div.contents:
                    if isinstance(content, str) and content != "\n":
                        result.append(content.replace("\n", " ").strip())
                    elif isinstance(content, Tag):
                        result.append(str(content.string).replace("\n", " "))
                results.append(result)
        return results

    def get_tag_text(self, tag_name: str, attrs: dict) -> str:
        tag = self.bs.find(name=tag_name, attrs=attrs)
        if tag and isinstance(tag, Tag):
            return tag.text
        return "-"

    def to_number(self, val: str) -> float | int:
        result = ''.join(chr for chr in val if chr.isdigit() or "." == chr)
        if result:
            if "." in val:
                return float(result)
            return int(result)
        return 0

    def get_table(self, attrs: dict | None = None, remove_header: bool = True) -> list[list[Tag]]:
        results: list[list[Tag]] = []
        table = self.bs.find(name="table", attrs=attrs)
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

    def convert_arr_to_str(self, arr: list[str]) -> str:
        return ",".join([val for val in list(dict.fromkeys(arr)) if val not in ["", " ", ',', "None", "None found,", "add some"]])

    def get_header(self) -> list[str]:
        return [field.name for field in fields(self) if field.name != "bs"]
