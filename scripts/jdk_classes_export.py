from typing import Dict, Tuple
from pathlib import Path
import re

import urllib3
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

_JDK_DOC_URL = 'https://docs.oracle.com/en/java/javase/11/docs/api/allclasses.html'
_PKG_DATA_REGEX = re.compile(r'(\w+) in ([\w\.]+)')

_TEMPLATE_PATH = Path(__file__).parent / 'templates' / 'class_type_data.jinja2'
_OUTPUT_PATH = Path(__file__).parent / '..' / 'crudhex' / 'domain' / 'services' / 'data' / 'class_type_data.py'


def _get_doc_html() -> str:
    http = urllib3.PoolManager()
    response = http.request('GET', _JDK_DOC_URL)
    return response.data.decode('utf-8')


def _parse_doc_data() -> Dict[str, str]:
    doc_html = _get_doc_html()
    soup = BeautifulSoup(doc_html, 'html.parser')
    types_list = soup.find('main', {'class': 'indexContainer'}).find('ul')
    types_data = {}
    for type_item in types_list.find_all('li'):
        type_data = type_item.find('a')
        type_name = type_data.text
        pkg_data = _parse_pkg_data(type_data['title'])

        print(f'Parsed {pkg_data[0]} {type_name} from package {pkg_data[1]}')
        types_data[type_name] = pkg_data[1]

    return types_data


def _parse_pkg_data(pkg_data: str) -> Tuple[str, str]:
    match = _PKG_DATA_REGEX.match(pkg_data)
    if not match:
        raise RuntimeError(f'Invalid package data: {pkg_data}')

    return match.group(1), match.group(2)


def _render_template(types_data: Dict[str, str]):
    env = Environment(loader=FileSystemLoader(_TEMPLATE_PATH.parent))
    template = env.get_template(_TEMPLATE_PATH.name)
    output = template.render(jdk_types=types_data)

    _OUTPUT_PATH.write_text(output)


if __name__ == '__main__':
    data = _parse_doc_data()
    _render_template(data)
    print('\n Types data generated successfully')
