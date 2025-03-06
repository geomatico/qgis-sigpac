import os
import shutil
import ssl
import subprocess
from typing import List
from urllib.error import URLError
from urllib.request import urlretrieve


def _unpack_file(src, dest, remove_source=True):
    shutil.unpack_archive(src, dest)
    if remove_source:
        os.remove(src)


def download_file(url, path, progress) -> str:
    file_path = os.path.join(path, os.path.basename(url))

    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        urlretrieve(url, file_path, progress)
        _unpack_file(file_path, path)
        return str(file_path)
    except URLError as e:
        raise BaseException(f"Error downloading file: {e}")


def download_multiple(urls: List[str], path, progress, total_progress = None) -> str:

    count = 0
    total = len(urls)
    downloaded_file_paths = []
    downloads_path = os.path.join(path, "downloads")
    os.makedirs(downloads_path, exist_ok=True)
    for url in urls:
        count = count + 1
        total_progress(count, total) if total_progress else None
        file_path = download_file(url, downloads_path, progress)
        downloaded_file_paths.append(file_path)

    return downloads_path


def merge_files(files_dir: str, path: str, progress) -> None:
    count = 0
    files = os.listdir(files_dir)
    total = len(files)
    for gpkg in files:
        count = count + 1
        progress(count, total)
        scr = os.path.join(files_dir, os.path.basename(gpkg))
        dest = os.path.join(path, 'output.gpkg')
        ogr_cmd = """ogr2ogr -update -append -f GPKG {} {}""" \
            .format(dest, scr)
        subprocess.run(ogr_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
