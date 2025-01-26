import os
import pathlib
import urllib.parse
from datetime import datetime

import requests
from dotenv import load_dotenv

NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
NASA_EPIC_URL = "https://api.nasa.gov/EPIC/api/natural"
NASA_EPIC_IMAGE_URL = "https://api.nasa.gov/EPIC/archive/natural/{year}/{month:02d}/{day:02d}/png/{image_name}.png?api_key={api_key}"


def fetch_spacex_last_launch_images():
    r = requests.get("https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a")
    r.raise_for_status()
    photo_links = r.json()['links']['flickr']['original']
    for idx, url in enumerate(photo_links):
        download_image(url, os.path.join("images", f'spacex_{idx}.jpg'))


def download_image(image_url, image_path):
    r = requests.get(image_url, headers={'User-agent': "test"})
    r.raise_for_status()
    pathlib.Path(image_path).parent.mkdir(parents=True, exist_ok=True)
    with open(image_path, 'wb') as f:
        f.write(r.content)


def fetch_file_extension(file_url):
    file_path_raw = urllib.parse.urlparse(file_url).path
    file_path_unquoted = urllib.parse.unquote(file_path_raw)
    _, file_name = os.path.split(file_path_unquoted)
    _, file_extension = os.path.splitext(file_name)
    return file_extension


def fetch_nasa_images(nasa_api_token, images_count):
    params = {'api_key': nasa_api_token, "count": images_count}
    r = requests.get(NASA_APOD_URL, params=params)
    r.raise_for_status()
    for id, data in enumerate(r.json()):
        image_url = data['url']
        image_extension = fetch_file_extension(image_url)
        download_image(image_url, os.path.join("images", f'nasa_apod_{id}' + image_extension))


def fetch_nasa_epic_images(nasa_api_token):
    params = {'api_key': nasa_api_token}
    r = requests.get(NASA_EPIC_URL, params=params)
    r.raise_for_status()
    for id, data in enumerate(r.json()):
        date = datetime.fromisoformat(data["date"])
        image_url = NASA_EPIC_IMAGE_URL.format(
            year=date.year, month=date.month, day=date.day, image_name=data["image"], api_key=nasa_api_token
        )
        download_image(image_url, os.path.join("images", f'nasa_epic_{id}.png'))


def main():
    download_image("https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg", "images/hubble.jpg")
    fetch_spacex_last_launch_images()
    load_dotenv()
    nasa_api_token = os.getenv("NASA_TOKEN")
    fetch_nasa_images(nasa_api_token, 30)
    fetch_nasa_epic_images(nasa_api_token)


if __name__ == '__main__':
    main()
