import argparse
import os
import pathlib
import urllib.parse
from datetime import datetime

import requests
from dotenv import load_dotenv

NASA_EPIC_URL = "https://api.nasa.gov/EPIC/api/natural"
NASA_EPIC_IMAGE_URL = "https://api.nasa.gov/EPIC/archive/natural/{year}/{month:02d}/{day:02d}/png/{image_name}.png?api_key={api_key}"


def fetch_file_extension(file_url):
    file_path_raw = urllib.parse.urlparse(file_url).path
    file_path_unquoted = urllib.parse.unquote(file_path_raw)
    _, file_name = os.path.split(file_path_unquoted)
    _, file_extension = os.path.splitext(file_name)
    return file_extension


def fetch_nasa_epic_images(nasa_api_token, image_directory):
    params = {'api_key': nasa_api_token}
    r = requests.get(NASA_EPIC_URL, params=params)
    r.raise_for_status()
    for id, data in enumerate(r.json()):
        date = datetime.fromisoformat(data["date"])
        image_url = NASA_EPIC_IMAGE_URL.format(
            year=date.year, month=date.month, day=date.day, image_name=data["image"], api_key=nasa_api_token
        )
        image_bytes = download_image(image_url)
        image_path = os.path.join(image_directory, f'nasa_epic_{id}.png')
        save_image(image_path, image_bytes)


def download_image(image_url):
    response = requests.get(image_url, headers={'User-agent': "test"})
    response.raise_for_status()
    return response.content


def save_image(image_path, image_bytes):
    pathlib.Path(image_path).parent.mkdir(parents=True, exist_ok=True)
    with open(image_path, 'wb') as f:
        f.write(image_bytes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_directory", help="directory for images download", default="images")
    args = parser.parse_args()
    load_dotenv()
    nasa_api_token = os.getenv("NASA_TOKEN")
    fetch_nasa_epic_images(nasa_api_token, args.image_directory)


if __name__ == '__main__':
    main()
