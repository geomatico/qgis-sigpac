import urllib.request
import os
from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QLineEdit)
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView
from qgis.PyQt.QtWebKit import QWebSettings

class SigPacLicenceAcceptBrowser(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.resize(800, 800)

        self.cookie = ''

        self.url = "https://www.fega.gob.es/orig/"

        layout = QVBoxLayout()

        # Widget para el navegador
        self.webview = QWebView(self)
        self.webview.load(QUrl(self.url))
        self.webview.page().networkAccessManager().finished.connect(self.network_request_done)

        self.webview.settings().setAttribute(QWebSettings.PluginsEnabled, True)

        layout.addWidget(self.webview)

        self.setLayout(layout)
        self.setWindowTitle("Acepte las condiciones")


    def network_request_done(self, request):
        if request.url().toString() == "https://www.fega.gob.es/atom/es.fega.sigpac.xml":
            self.cookie = request.request().rawHeader(b'Cookie')
            #TODO: we should manage if everything is ok
            self.accept()

