from pathlib import Path
import xml.etree.ElementTree as ET


ns = {
    'atom': 'http://www.w3.org/2005/Atom',
    'inspire_dls': 'http://inspire.ec.europa.eu/schemas/inspire_dls/1.0'
}

general_data = []

def extract_general_data(xml_string, url=""):

    if not len(general_data):
        try:
            atomroot = ET.fromstring(xml_string)
            for x in atomroot.findall('atom:entry', ns):
                title = x.find('atom:title', ns).text
                links = x.findall('atom:link', ns)
                for link in links:
                    if link.attrib['rel'] == 'enclosure' and link.attrib['type'] == 'application/atom+xml':
                        url = link.attrib['href']
                        general_data.append({'title': title, 'url': url})
        except BaseException as e:
            raise BaseException(f'Failed to extract general data from {url}: {e}')

    return general_data


def main(xml_string):
    results = extract_general_data(xml_string)
    print(results)
    return results


if __name__ == "__main__":
    with Path.open("es.fega.sigpac.xml", encoding="utf-8") as file:
        xml_string = file.read()
    main(xml_string)

