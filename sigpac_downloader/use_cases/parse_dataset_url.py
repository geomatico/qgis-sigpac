from sigpac_downloader.etl.atom_dataset_parser import extract_dataset_url
from sigpac_downloader.services.get_url import get_url

def parse_dataset_url(url: str):
    raw_data = get_url(url)
    dataset_url = extract_dataset_url(raw_data)
    return dataset_url

def main(url: str):
    dataset_url = parse_dataset_url(url)
    print(dataset_url)
    return dataset_url

if __name__ == "__main__":
    main("https://www.fega.gob.es/atom/es.fega.sigpac.ld.2024.xml")