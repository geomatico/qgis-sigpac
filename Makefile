
PLUGINNAME = sigpac_downloader

RESOURCE_SRC=$(shell grep '^ *<file' resources.qrc | sed 's@</file>@@g;s/.*>//g' | tr '\n' ' ')

#VERSION=$(shell cat sigpac_downloader/metadata.txt | awk -F= '/^version/{print $2}')
VERSION=$(shell cat sigpac_downloader/metadata.txt | awk -F '=' '/^version/{print $$NF}')

package:
	rm -f $(PLUGINNAME)*.zip
	zip -9r $(PLUGINNAME)-$(VERSION).zip $(PLUGINNAME)
	echo "Created package: $(PLUGINNAME)-$(VERSION).zip"
