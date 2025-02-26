# @file        html_municipality_parser.py
# @author      iCarto <info@icarto.es>
# @license     MIT License (c) 2025 iCarto
#  Permission is granted to use, copy, modify, and distribute this software
# under the MIT License. See the LICENSE file for details.

import html.parser
import urllib.parse
from pathlib import Path


class FileListParser(html.parser.HTMLParser):
    def __init__(self, base_url=""):
        super().__init__()
        self.files = []
        self.current_row = []
        self.in_table = False
        self.column_count = 0
        self.base_url = base_url

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True

        if self.in_table and tag == "tr":
            self.current_row = []
            self.column_count = 0

        if tag == "a" and self.in_table:
            for attr in attrs:
                if attr[0] == "href":
                    self.current_row.append(attr[1])

    def handle_data(self, data):
        if self.in_table:
            cleaned_data = data.strip()
            if cleaned_data:
                self.current_row.append(cleaned_data)
            self.column_count += 1

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False

        if tag == "tr" and self.in_table:
            if (
                len(self.current_row) == 4
                and "_shp" not in self.current_row[1]
                and self.current_row[3].strip() != "-"
            ):
                _href = self.current_row[0]
                href = (
                    urllib.parse.urljoin(self.base_url, _href)
                    if self.base_url
                    else _href
                )
                self.files.append(
                    {
                        "name": self.current_row[1],
                        "href": href,
                        "last_modified": self.current_row[2],
                        "size": self.current_row[3],
                    }
                )

            self.current_row = []


def extract_municipality_data(html_string, url=""):
    parser = FileListParser(url)
    parser.feed(html_string)
    return parser.files


def main(html_string):
    results = extract_municipality_data(html_string)
    print(results)
    return results


if __name__ == "__main__":
    with Path.open("rec_2024_39-CANTABRIA.html", encoding="utf-8") as file:
        html_string = file.read()
    main(html_string)
