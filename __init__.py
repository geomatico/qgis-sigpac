# -*- coding: utf-8 -*-
"""
/***************************************************************************
 sigpac_downloader
                                 A QGIS plugin
 Plugin to download SIGPAC parcels
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-01-20
        copyright            : (C) 2022 by Geomatico
        email                : info@geomatico.es
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load sigpac_downloader class from file sigpac_downloader.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .sigpac_downloader import sigpac_downloader
    return sigpac_downloader(iface)
