from sigpac_downloader.etl.html_municipality_parser import extract_municipality_data
from sigpac_downloader.services.get_url import get_url


def parse_municipality_data(url: str):
    raw_data = get_url(url)
    municipalities = extract_municipality_data(raw_data, url)
    return municipalities

def main(url: str):
    municipalities = parse_municipality_data(url)
    print(municipalities)
    return municipalities

if __name__ == "__main__":
    main("https://www.fega.gob.es/atom/2024/rec_2024/01%20-%20ALAVA/")