# -*- coding: utf-8 -*-
"""
/***************************************************************************
 sigpac_downloaderDialog
                                 A QGIS plugin
 Plugin to download SIGPAC parcels
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-01-20
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Geomatico
        email                : info@geomatico.es
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import urllib
from urllib.error import URLError

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from .sigpac_licence_accept_browser import SigPacLicenceAcceptBrowser

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
pluginPath = os.path.split(os.path.dirname(__file__))[0]
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    pluginPath, 'ui', 'main_window.ui'))

from .listamuni import *

listProvincias = LISTPROV
listMunicipios = LISTMUNI

class main_window(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(main_window, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.browser = None
        self.comboBox_province.clear()
        self.comboBox_municipality.clear()
        self.comboBox_province.addItems(listProvincias)
        self.comboBox_province.currentIndexChanged.connect(self.filter_municipality)

        self.btnOpenBrowser.clicked.connect(self.openBrowser)

        self.pushButton.clicked.connect(self.downloadFile)

    def openBrowser(self):
        self.browser = SigPacLicenceAcceptBrowser()
        conditionsAccepted = self.browser.exec_()
        if conditionsAccepted == 1:
            self.btnOpenBrowser.setStyleSheet("background-color:#00ff00;");


    def getDownloadUrl(self):

        inecode_catastro = self.comboBox_municipality.currentText()

        if inecode_catastro == '':
            return None
        codprov = inecode_catastro[0:2]
        codmuni = inecode_catastro[0:5]

        # url = 'https://www.fega.gob.es/atom/07/07011_20210104.zip'
        # TODO: should retrieve URL from ATOM https://www.fega.gob.es/atom/07/es.fega.sigpac.07.xml to gate proper date
        url = u'https://www.fega.gob.es/atom/%s/%s_20210104.zip' % (
            codprov, codmuni)
        return url

    def downloadFile(self):

        url = self.getDownloadUrl()
        if url == None:
            self.displayWarning('Debes seleccionar provincia y municipio')
            return

        if self.browser and self.browser.cookie:
            opener = urllib.request.build_opener()
            opener.addheaders = [('Cookie', self.browser.cookie)]
            urllib.request.install_opener(opener)
            file_path = os.path.join(self.mQgsFileWidget.filePath(),
                                     os.path.basename(url))
            #file_path = os.path.join('/home/marti/Descargas/pruebas_sigpac', os.path.basename(url))
            try:
                urllib.request.urlretrieve(url, file_path)
                self.displayWarning('')
            except URLError as e:
                raise RuntimeError("Failed to download '{}'. '{}'".format(url, e.reason))

        else:
            self.displayWarning('Debes aceptar las condiciones')


    def filter_municipality(self, index):
        """Message for fields without information"""

        filtroprovincia = self.comboBox_province.currentText()
        self.comboBox_municipality.clear()

        self.comboBox_municipality.addItems([muni for muni in listMunicipios if muni[0:2] == filtroprovincia[0:2]])


    def displayWarning(self, text):
        # warning: conditions not accepted
        self.label.setText(text)