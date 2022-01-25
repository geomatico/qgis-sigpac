import urllib.request
import os
from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QLineEdit)
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

class SigPacLicenceAcceptBrowser(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.resize(800, 800)

        self.url = "https://www.fega.gob.es/orig/"

        layout = QVBoxLayout()

        # Widget para el navegador
        self.webview = QWebView(self)
        self.webview.load(QUrl(self.url))
        self.webview.page().networkAccessManager().finished.connect(self.network_request_done)


        layout.addWidget(self.webview)

        self.setLayout(layout)
        self.setWindowTitle("Acepte las condiciones")


    def network_request_done(self, request):
        if request.url().toString() == "https://www.fega.gob.es/atom/es.fega.sigpac.xml":
            cookie = request.request().rawHeader(b'Cookie')

            opener = urllib.request.build_opener()
            opener.addheaders = [('Cookie', cookie)]
            urllib.request.install_opener(opener)
            file_path = os.path.join('/home/fran/Descargas/pruebas_sigpac', os.path.basename('https://www.fega.gob.es/atom/07/07011_20210104.zip'))
            urllib.request.urlretrieve('https://www.fega.gob.es/atom/07/07011_20210104.zip', file_path)

