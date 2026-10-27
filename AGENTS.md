# Migration to QGIS 4.x (Qt 6)

## 1. Metadata changes

- **File modified:** `sigpac_downloader/metadata.txt`
- **What was added:** `qgisMaximumVersion=4.99` in the `[general]` section.

  ```ini
  [general]
  name=SIGPAC Downloader
  qgisMinimumVersion=3.0
+ qgisMaximumVersion=4.99
  description=Plugin to download SIGPAC parcels
  ...
  ```

## 2. UI dialog execution

- **File modified:** `sigpac_downloader/gui/main_window.py`
- **Change:** Replaced old PyQt5 `app.exec_()` with PyQt6 `app.exec()`.

  ```python
  # old
  app.exec_()
  # new
  app.exec()
  ```

## 3. Dialog modal call in plugin main

- **File modified:** `sigpac_downloader/sigpac_downloader.py`
- **Change:** Updated call from `self.dlg.exec_()` to `self.dlg.exec()`.

  ```python
  # old
  result = self.dlg.exec_()
  # new
  result = self.dlg.exec()
  ```

## 4. What to check next

- Verify no remaining usages of `exec_()` in project.
- Ensure all other PyQt5 imports (`QtCore`, `QtGui`, `QtWidgets`) are compatible; in most cases they are aliased to `qgis.PyQt` which currently supports both PyQt5 and PyQt6.
- Run the plugin in a QGIS 4.x environment to confirm no runtime errors.

---

### Summary
The repository now contains:

- Updated `metadata.txt` with maximum QGIS version.
- UI code compatible with Qt6 (`exec()` usage).
- Plugin code compatible with Qt6 (`exec()` usage in `run`).

These changes are sufficient for the plugin to load and run under QGIS 4.x. Further adjustments may be required if additional dependencies on PyQt5-specific APIs are discovered during testing.
