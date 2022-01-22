import requests
import urllib.parse as parse

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


def search_godville_crossword(_search):
    encoded_search = parse.quote(_search.encode('utf8'))
    response = requests.get(f"http://godb.shouhei.ru/query.php?str={encoded_search}&re=1&cr=on&ct=0")
    text = response.text

    parsed_html = BeautifulSoup(text, "html.parser")
    results = parsed_html.find_all('li')

    for li in results:
        contents = li.contents[0]
        if isinstance(contents, NavigableString):
            yield contents
        elif isinstance(contents, Tag) and contents.name == "b":
            yield contents.contents[0]
