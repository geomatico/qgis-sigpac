from sigpac_downloader.etl.html_province_parser import extract_province_data
from sigpac_downloader.services.get_url import get_url


def parse_province_data(url: str):
    raw_data = get_url(url)
    provinces = extract_province_data(raw_data, url)
    return provinces

def main(url: str):
    provinces = parse_province_data(url)
    print(provinces)
    return provinces

if __name__ == "__main__":
    main("https://www.fega.gob.es/atom/2024/rec_2024/")