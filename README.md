# SIGPAC (Spain Agricultural Plots) Downloader

The Agricultural Plot Geographic Information System (SIGPAC) enables the geographic identification of plots declared by farmers and livestock farmers in Spain. More info: https://www.fega.gob.es/en/rural-development/sigpac-aplication

This plugin allows the user to easily download the plots of every municipality. Prior to that, the Terms&Conditions of the web page must be accepted and a download directory must be selected.

The SIGPAC Downloader uses the ATOM service according to the Inspire Directive.

Special Thanks to [@fpuga](https://github.com/fpuga) from [iCarto](https://icarto.es/) for provide the etl code!


## Make the package to upload to qgis plugins site

```shell
make package
```

## Run plugin on qgis version to test

Inside docker folder, exists a `docker-compose.yml` with a qgis service pointing to the latest ltr version. 
You can change to other than exists on [qgis offical docker hub image](https://hub.docker.com/r/qgis/qgis).

Exeuting `start_qgis.sh` will launch that version of QGIS with the sigpac-downloader plugin configured.
