from sigpac_downloader.etl.atom_general_parser import extract_general_data
from sigpac_downloader.services.get_url import get_url

atom_url = f'https://www.fega.gob.es/atom/es.fega.sigpac.xml'

def parse_general_data(url: str = atom_url):
    raw_data = get_url(url)
    general_data = extract_general_data(raw_data, url)
    return general_data

def main(url: str):
    general_data = parse_general_data(url)
    print(general_data)
    return general_data

if __name__ == "__main__":
    main("https://www.fega.gob.es/atom/es.fega.sigpac.xml")