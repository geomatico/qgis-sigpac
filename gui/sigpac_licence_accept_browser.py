import urllib.request
import os
from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QLineEdit)
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView
from qgis.PyQt.QtWebKit import QWebSettings
from urllib.request import urlopen, Request

# import sys
# from PyQt5.QtWidgets import QApplication

class SigPacLicenceAcceptBrowser(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.resize(800, 800)
        self.setModal(False)

        self.cookie = ''
        self.firstLoad = True

        self.url = "https://www.fega.gob.es/orig/"

        layout = QVBoxLayout()

        # Widget para el navegador
        self.webview = QWebView(self)
        self.webview.page().networkAccessManager().finished.connect(self.network_request_done)
        #self.webview.loadStarted.connect(self.loaded)

        webSettings = self.webview.settings()
        webSettings.clearMemoryCaches()

        self.webview.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        self.webview.load(QUrl(self.url))

        layout.addWidget(self.webview)

        self.setLayout(layout)
        self.setWindowTitle("Acepte las condiciones")


    def network_request_done(self, reply):
        if reply.url().toString() == 'https://www.fega.gob.es/atom/es.fega.sigpac.xml':
            self.cookie = reply.request().rawHeader(b'Cookie')
            self.accept()
