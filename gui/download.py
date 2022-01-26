import sys
from PyQt5.QtCore import QFile, QUrl
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QWidget, QApplication
from PyQt5.QtWebKitWidgets import QWebView

from urllib.error import URLError
from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        vlay = QVBoxLayout(self)
        self.le = QLineEdit()
        self.le.setText('https://www.fega.gob.es/orig/')
        self.browser = QWebView()
        self.le.returnPressed.connect(self.on_return_pressed)
        self.browser.page().setForwardUnsupportedContent(True)
        self.browser.page().unsupportedContent.connect(self.on_unsupportedContent)
        self.browser.page().networkAccessManager().finished.connect(self.network_request_done)


        vlay.addWidget(self.le)
        vlay.addWidget(self.browser)

        self.setLayout(vlay)

    def on_return_pressed(self):
        self.browser.load(QUrl(self.le.text()))

    def on_unsupportedContent(self, request):
        reply = self.browser.page().networkAccessManager().get(request)
        reply.finished.connect(self.on_finished)

    def on_finished(self):
        reply = self.sender()
        ba = reply.readAll()
        fileName = reply.url().fileName()
        file = QFile(fileName)
        if file.open(QFile.WriteOnly):
            file.write(ba)
            file.close()
        reply.deleteLater()

    def network_request_done(self, request):
        if request.url().toString() == "https://www.fega.gob.es/atom/es.fega.sigpac.xml":
            cookie = request.request().rawHeader(b'Cookie')


            codprov = '36'

            if codprov:
                atom_url = f'https://www.fega.gob.es/atom/{codprov}/es.fega.sigpac.{codprov}.xml'
                request = Request(atom_url)
                request.add_header('Cookie', cookie)
                file = urlopen(request)
                data = file.read()
                file.close()

                ns = {'atom': 'http://www.w3.org/2005/Atom', 'inspire_dls': 'http://inspire.ec.europa.eu/schemas/inspire_dls/1.0'}
                atomroot = ET.fromstring(data)

                gpkg_links = {}

                for x in atomroot.findall('atom:entry', ns):
                    cod = x.find('inspire_dls:spatial_dataset_identifier_code', ns).text.replace('es.fega.sigpac.', '')
                    links = x.findall('atom:link', ns)
                    for link in links:
                        if link.attrib['type'] == 'application/geopackage+vnd.sqlite3':
                            gpkg_links[cod] = link.attrib['href']

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())