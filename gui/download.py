import sys
from PyQt5.QtCore import QFile, QUrl
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QWidget, QApplication
from PyQt5.QtWebKitWidgets import QWebView

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
            print(request.request().rawHeader(b'Cookie'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())