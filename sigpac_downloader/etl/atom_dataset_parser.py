from pathlib import Path
import xml.etree.ElementTree as ET


ns = {
    'atom': 'http://www.w3.org/2005/Atom',
    'inspire_dls': 'http://inspire.ec.europa.eu/schemas/inspire_dls/1.0'
}

def extract_dataset_url(xml_string, url="") -> str:

    url = ""

    try:
        atomroot = ET.fromstring(xml_string)
        for x in atomroot.findall('atom:entry', ns):
            links = x.findall('atom:link', ns)
            for link in links:
                if link.attrib['rel'] == 'enclosure':
                    url = link.attrib['href'] + '/'
                    return url
    except BaseException as e:
        raise BaseException(f'Failed to extract general data from {url}: {e}')



def main(xml_string):
    results = extract_dataset_url(xml_string)
    print(results)
    return results


if __name__ == "__main__":
    with Path.open("es.fega.sigpac.xml", encoding="utf-8") as file:
        xml_string = file.read()
    main(xml_string)

