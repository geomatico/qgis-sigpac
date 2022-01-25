import urllib
import os
from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QLineEdit)
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

class DlgBrowserSigpac(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.resize(800, 800)

        self.url = "https://www.fega.gob.es/orig/"

        layout = QVBoxLayout()

        # Widget para el navegador
        self.webview = QWebView(self)
        self.webview.load(QUrl(self.url))
        self.webview.urlChanged.connect(self.setUrl)
        self.webview.loadFinished.connect(self._result_available)


        layout.addWidget(self.webview)

        self.setLayout(layout)
        self.setWindowTitle("Acepte las condiciones")

    def _result_available(self, ok):
        frame = self.webview.page().mainFrame()
        if self.url.toString() == "https://www.fega.gob.es/atom/es.fega.sigpac.xml":
            print(frame.toHtml())

            zippath = self.dlg.lineEdit_path.text()
            wd = os.path.join(zippath, 'downloads')

            zipParcels = os.path.join(wd, "kk.zip")
            urllib.request.urlretrieve('https://www.fega.gob.es/atom/07/07011_20210104.zip', zipParcels, self.reporthook)

    def setUrl(self, url):
        self.url = url

