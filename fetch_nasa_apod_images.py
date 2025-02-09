import argparse
import os
import pathlib
import urllib.parse

import requests
from dotenv import load_dotenv

NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
NASA_EPIC_IMAGE_URL = "https://api.nasa.gov/EPIC/archive/natural/{year}/{month:02d}/{day:02d}/png/{image_name}.png?api_key={api_key}"


def download_image(image_url):
    response = requests.get(image_url, headers={'User-agent': "test"})
    response.raise_for_status()
    return response.content


def save_image(image_path, image_bytes):
    pathlib.Path(image_path).parent.mkdir(parents=True, exist_ok=True)
    with open(image_path, 'wb') as f:
        f.write(image_bytes)


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
    for id, image_data in enumerate(response.json()):
        image_extension = fetch_file_extension(image_data['url'])
        image_store_path = os.path.join(images_directory_path, f'nasa_apod_{id}' + image_extension)
        image_bytes = download_image(image_data['url'])
        save_image(image_store_path, image_bytes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_directory", help="directory for images download", default="images")
    parser.add_argument("--image_count", help="images download count", type=int, default=30)
    args = parser.parse_args()
    load_dotenv()
    nasa_api_token = os.getenv("NASA_TOKEN")
    fetch_images(nasa_api_token, args.image_count, args.image_directory)


if __name__ == '__main__':
    main()
