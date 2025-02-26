
PLUGINNAME = sigpac_downloader

VERSION=$(shell cat sigpac_downloader/metadata.txt | awk -F '=' '/^version/{print $$NF}')

package:
	rm -f $(PLUGINNAME)*.zip
	zip -9r $(PLUGINNAME)-$(VERSION).zip $(PLUGINNAME)
	echo "Created package: $(PLUGINNAME)-$(VERSION).zip"
