import argparse
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from image_utils import download_image, save_image
from nasa_api_token_utils import get_nasa_api_token

NASA_EPIC_URL = "https://api.nasa.gov/EPIC/api/natural"
NASA_EPIC_IMAGE_URL_TEMPLATE = "https://api.nasa.gov/EPIC/archive/natural/{year}/{month:02d}/{day:02d}/png/{image_name}.png"


def fetch_nasa_epic_images(nasa_api_token, image_directory):
    params = {'api_key': nasa_api_token}
    response = requests.get(NASA_EPIC_URL, params=params)
    response.raise_for_status()
    for image_id, data in enumerate(response.json()):
        date = datetime.fromisoformat(data["date"])
        image_url = NASA_EPIC_IMAGE_URL_TEMPLATE.format(
            year=date.year, month=date.month, day=date.day, image_name=data["image"]
        )
        image_bytes = download_image(image_url, {'api_key': nasa_api_token})
        image_path = os.path.join(image_directory, f'nasa_epic_{image_id}.png')
        save_image(image_path, image_bytes)


def main():
    parser = argparse.ArgumentParser(
        prog="fetch_nasa_epic_images.py",
        description="Downloads images from nasa epic resource https://api.nasa.gov/EPIC/api/natural",
    )
    parser.add_argument("--image_directory", help="directory for images download", default="images")
    args = parser.parse_args()
    load_dotenv()
    nasa_api_token = get_nasa_api_token()
    fetch_nasa_epic_images(nasa_api_token, args.image_directory)


if __name__ == '__main__':
    main()
