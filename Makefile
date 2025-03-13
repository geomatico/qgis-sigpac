
PLUGINNAME = sigpac_downloader

VERSION=$(shell cat sigpac_downloader/metadata.txt | awk -F '=' '/^version/{print $$NF}')

package:
	rm -f build/$(PLUGINNAME)*.zip
	mkdir -p build
	cp -r $(PLUGINNAME) build/
	cp LICENSE README.md build/$(PLUGINNAME)/
	cd build && zip -9r $(PLUGINNAME)-$(VERSION).zip $(PLUGINNAME) && rm -rf $(PLUGINNAME)
	echo "Created package: $(PLUGINNAME)-$(VERSION).zip"
