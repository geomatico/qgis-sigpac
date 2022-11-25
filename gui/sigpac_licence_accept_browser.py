import urllib.request
import os
from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QLineEdit)
from qgis.PyQt.QtCore import QUrl, pyqtSignal
from qgis.PyQt.QtWebKitWidgets import QWebView, QWebInspector
from qgis.PyQt.QtWebKit import QWebSettings


class SigPacLicenceAcceptBrowser(QDialog):
    conditionsAccepted = pyqtSignal(str)

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

        webSettings = self.webview.settings()
        webSettings.clearMemoryCaches()

        self.webview.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        # self.webview.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        self.webview.settings().setAttribute(QWebSettings.JavascriptEnabled, True)

        # inspector = QWebInspector()
        # inspector.setPage(self.webview.page())
        # inspector.setVisible(True)


        self.webview.load(QUrl(self.url))

        layout.addWidget(self.webview)
        # layout.addWidget(inspector)

        self.setLayout(layout)
        self.setWindowTitle("Acepte las condiciones")


    def network_request_done(self, reply):
        if reply.url().toString() == 'https://www.fega.gob.es/atom/es.fega.sigpac.xml':
            self.cookie = reply.request().rawHeader(b'Cookie')
            self.conditionsAccepted.emit(self.cookie)
            self.accept()
