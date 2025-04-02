import os
import pathlib
import urllib

import requests

def fetch_file_extension(file_url):
    file_path_raw = urllib.parse.urlparse(file_url).path
    file_path_unquoted = urllib.parse.unquote(file_path_raw)
    _, file_name = os.path.split(file_path_unquoted)
    _, file_extension = os.path.splitext(file_name)
    return file_extension

def download_image(image_url, params=None):
    response = requests.get(image_url, headers={'User-agent': "test"}, params=params)
    response.raise_for_status()
    return response.content


def save_image(image_path, image_bytes):
    pathlib.Path(image_path).parent.mkdir(parents=True, exist_ok=True)
    with open(image_path, 'wb') as f:
        f.write(image_bytes)
