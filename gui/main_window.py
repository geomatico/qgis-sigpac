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
from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET
import threading

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from .sigpac_licence_accept_browser import SigPacLicenceAcceptBrowser

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
pluginPath = os.path.split(os.path.dirname(__file__))[0]
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    pluginPath, 'ui', 'main_window.ui'))

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
        self.comboBox_province.currentIndexChanged.connect(self.download_and_parse_province_atom)
        self.comboBox_municipality.currentIndexChanged.connect(self.update_file_options_for_municipality)

        self.btnOpenBrowser.clicked.connect(self.openBrowser)

        self.btnDownload.clicked.connect(self.downloadFile)

        self.providerLabel.setOpenExternalLinks(True)
        self.conditionsLabel.setOpenExternalLinks(True)

        self.provinces = {}
        self.links = {}

    def openBrowser(self):
        self.browser = SigPacLicenceAcceptBrowser()
        conditionsAccepted = self.browser.exec_()
        if conditionsAccepted == 1:
            self.download_and_parse_general_atom()
            self.btnOpenBrowser.setStyleSheet("background-color:#00ff00;")
            self.btnOpenBrowser.setText('Condiciones Aceptadas')
            self.activateControls()


    def activateControls(self):
        self.btnOpenBrowser.setEnabled(False)
        self.comboBox_municipality.setEnabled(True)
        self.comboBox_province.setEnabled(True)
        self.comboBox_files.setEnabled(True)
        self.mQgsFileWidget.setEnabled(True)
        self.btnDownload.setEnabled(True)


    def getSelectedProvinceLink(self):
        if self.comboBox_province.currentText() != '':
            return self.provinces[self.comboBox_province.currentText()]

    def getSelectedMunicipalityFileLink(self):
        municipality = self.comboBox_municipality.currentText()
        file = self.comboBox_files.currentText()
        if municipality != '':
            if file != '':
                return self.links[municipality][file]


    def downloadFile(self):

        path = self.mQgsFileWidget.filePath()
        url = self.getSelectedMunicipalityFileLink()

        if url == None:
            self.displayWarning('Debes seleccionar provincia y municipio')
            return

        if path == '':
            self.displayWarning('Debes seleccionar una carpeta de destino')
            return

        if self.browser and self.browser.cookie:
            self.displayWarning(f'Descargando {os.path.basename(url)}')
            opener = urllib.request.build_opener()
            opener.addheaders = [('Cookie', self.browser.cookie)]
            urllib.request.install_opener(opener)
            file_path = os.path.join(path, os.path.basename(url))

            self.displayWarning(f'Descargando...')
            self.progressBar.setEnabled(True)
            try:
                urllib.request.urlretrieve(url, file_path, self.updateProgress)
                self.displayWarning(f'Descarga correcta {os.path.basename(url)}')
            except URLError as e:
                self.displayWarning('Error en la descarga', True)
            self.progressBar.setEnabled(False)
        else:
            self.displayWarning('Debes aceptar las condiciones')


    def updateProgress(self, block_num, block_size, total_size):
        self.progressBar.setMaximum(total_size)
        downloaded = block_num * block_size
        if downloaded < total_size:
            self.progressBar.setValue(downloaded)


    def displayWarning(self, text, error=False):
        # warning: conditions not accepted
        if type(text) == str:
            self.lblInfo.setText(text)
        else:
            self.lblInfo.setText('')

        #color
        if error == True:
            self.lblInfo.setStyleSheet("color: red;")
        else:
            self.lblInfo.setStyleSheet("color: black;")

    def download_and_parse_general_atom(self):

        atom_url = f'https://www.fega.gob.es/atom/es.fega.sigpac.xml'
        request = Request(atom_url)
        request.add_header('Cookie', self.browser.cookie)
        try:
            file = urlopen(request)
            data = file.read()
            file.close()
        except:
            self.displayWarning('Error descargando el fichero atom general')
            return

        ns = {'atom': 'http://www.w3.org/2005/Atom',
              'inspire_dls': 'http://inspire.ec.europa.eu/schemas/inspire_dls/1.0'}

        try:
            atomroot = ET.fromstring(data)
            for x in atomroot.findall('atom:entry', ns):
                #if x.find('atom:title', ns).text != 'Tablas de códigos SIGPAC':
                title = x.find('atom:title', ns).text
                links = x.findall('atom:link', ns)
                for link in links:
                    if link.attrib['rel'] == 'enclosure' and link.attrib['type'] == 'application/atom+xml':
                        self.provinces[title] = link.attrib['href']
                        self.comboBox_province.addItem(title)
        except:
            self.displayWarning('Error leyendo el fichero atom general')
            return


    def download_and_parse_province_atom(self):
        atom_url = self.getSelectedProvinceLink()
        self.comboBox_municipality.clear()

        if atom_url:
            request = Request(atom_url)
            request.add_header('Cookie', self.browser.cookie)
            try:
                file = urlopen(request)
                data = file.read()
                file.close()
            except:
                self.displayWarning('Error descargando el fichero de provincia')
                return

            ns = {'atom': 'http://www.w3.org/2005/Atom',
                  'inspire_dls': 'http://inspire.ec.europa.eu/schemas/inspire_dls/1.0'}

            try:
                atomroot = ET.fromstring(data)
                for x in atomroot.findall('atom:entry', ns):
                    #cod = x.find('inspire_dls:spatial_dataset_identifier_code', ns).text.replace('es.fega.sigpac.', '')
                    title = x.find('atom:title', ns).text
                    links = x.findall('atom:link', ns)
                    download_links = {}
                    for link in links:
                        if link.attrib['rel'] == 'enclosure':
                            url = link.attrib['href']
                            file_type_text = 'GeoPackage' if link.attrib['type'] == 'application/geopackage+vnd.sqlite3' else \
                                'Shapefile' if link.attrib['type'] == 'application/x-shapefile' else \
                                'Otro'
                            file_title = f'{file_type_text}: {os.path.basename(url)} '
                            download_links[file_title] = url
                        if len(download_links.keys()):
                            self.links[title] = download_links
                    self.comboBox_municipality.addItem(title)
            except:
                self.displayWarning('Error leyendo el fichero de provincia')
                return

    def update_file_options_for_municipality(self):
        self.comboBox_files.clear()
        municipality = self.comboBox_municipality.currentText()
        if municipality:
            for file_title in self.links[municipality].keys():
                self.comboBox_files.addItem(file_title)



