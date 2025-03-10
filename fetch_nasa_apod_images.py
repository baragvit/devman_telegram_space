import argparse
import os
import urllib.parse

import requests
from dotenv import load_dotenv

from image_utils import get_nasa_api_token, download_image, save_image

NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"

def fetch_file_extension(file_url):
    file_path_raw = urllib.parse.urlparse(file_url).path
    file_path_unquoted = urllib.parse.unquote(file_path_raw)
    _, file_name = os.path.split(file_path_unquoted)
    _, file_extension = os.path.splitext(file_name)
    return file_extension


def fetch_images(nasa_api_token, images_count, images_directory_path):
    params = {'api_key': nasa_api_token, "count": images_count}
    response = requests.get(NASA_APOD_URL, params=params)
    response.raise_for_status()
    for image_id, image_data in enumerate(response.json()):
        image_extension = fetch_file_extension(image_data['url'])
        image_store_path = os.path.join(images_directory_path, f'nasa_apod_{image_id}.{image_extension}')
        image_bytes = download_image(image_data['url'])
        save_image(image_store_path, image_bytes)


def main():
    parser = argparse.ArgumentParser(
        prog="fetch_nasa_apod_images.py",
        description="Downloads images from nasa apod resource https://api.nasa.gov/planetary/apod",
    )
    parser.add_argument("--image_directory", help="directory for images download", default="images")
    parser.add_argument("--image_count", help="images download count", type=int, default=30)
    args = parser.parse_args()
    load_dotenv()
    nasa_api_token = get_nasa_api_token()
    fetch_images(nasa_api_token, args.image_count, args.image_directory)


if __name__ == '__main__':
    main()
