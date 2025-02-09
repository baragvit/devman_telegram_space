import argparse
import os
import pathlib

import requests


def fetch_images(launch_id, image_directory):
    photo_links = fetch_image_links(launch_id)
    for idx, url in enumerate(photo_links):
        image_store_path = os.path.join(image_directory, f'spacex_{idx}.jpg')
        image_bytes = download_image(url)
        save_image(image_store_path, image_bytes)


def fetch_image_links(launch_id):
    r = requests.get(f"https://api.spacexdata.com/v5/launches/{launch_id}")
    r.raise_for_status()
    photo_links = r.json()['links']['flickr']['original']
    return photo_links


def save_image(image_path, image_bytes):
    pathlib.Path(image_path).parent.mkdir(parents=True, exist_ok=True)
    with open(image_path, 'wb') as f:
        f.write(image_bytes)


def download_image(image_url):
    response = requests.get(image_url, headers={'User-agent': "test"})
    response.raise_for_status()
    return response.content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("launch_id", help="SpaceX launch id", nargs="?", default="latest")
    parser.add_argument("--image_directory", help="directory for images download", default="images")
    args = parser.parse_args()
    fetch_images(args.launch_id, args.image_directory)


if __name__ == '__main__':
    main()
