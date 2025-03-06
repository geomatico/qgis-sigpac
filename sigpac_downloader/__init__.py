# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load sigpac_downloader class from file sigpac_downloader.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from sigpac_downloader.sigpac_downloader import sigpac_downloader
    return sigpac_downloader(iface)