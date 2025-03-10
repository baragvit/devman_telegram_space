import argparse
import os

import requests

from image_utils import download_image, save_image


def fetch_images(photo_links, image_directory):
    for idx, url in enumerate(photo_links):
        image_store_path = os.path.join(image_directory, f'spacex_{idx}.jpg')
        image_bytes = download_image(url)
        save_image(image_store_path, image_bytes)


def fetch_image_links(launch_id):
    response = requests.get(f"https://api.spacexdata.com/v5/launches/{launch_id}")
    response.raise_for_status()
    photo_links = response.json()['links']['flickr']['original']
    return photo_links


def main():
    parser = argparse.ArgumentParser(
        prog="fetch_spacex_images.py",
        description="Downloads images from SpaceX resource https://api.spacexdata.com"
    )
    parser.add_argument("launch_id", help="SpaceX launch id", nargs="?", default="latest")
    parser.add_argument("--image_directory", help="directory for images download", default="images")
    args = parser.parse_args()
    photo_links = fetch_image_links(args.launch_id)
    fetch_images(photo_links, args.image_directory)


if __name__ == '__main__':
    main()
