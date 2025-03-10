import os
import pathlib

import requests


def download_image(image_url, params=None):
    if params is None:
        params = {}
    response = requests.get(image_url, headers={'User-agent': "test"}, params=params)
    response.raise_for_status()
    return response.content


def save_image(image_path, image_bytes):
    pathlib.Path(image_path).parent.mkdir(parents=True, exist_ok=True)
    with open(image_path, 'wb') as f:
        f.write(image_bytes)


def get_nasa_api_token():
    nasa_api_token = os.getenv("NASA_TOKEN")
    if not nasa_api_token:
        raise NasaApiTokenNotFoundException("Api token should be provided as environment variable NASA_TOKEN")
    return nasa_api_token


class NasaApiTokenNotFoundException(Exception):
    pass
