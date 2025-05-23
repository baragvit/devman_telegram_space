import argparse
import os
import random
from time import sleep

import telegram
from PIL import Image
from dotenv import load_dotenv

RESIZED_IMAGE_RESOLUTION = (256, 256)

MAX_AVAILABLE_TELEGRAM_IMAGE_SIZE = 20 * 1024 * 1024


class ImagesNotExist(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_shuffled_image_paths(image_directory_path):
    image_files = os.listdir(image_directory_path)
    if not image_files:
        raise ImagesNotExist(f"Image files not found in {os.path.abspath(image_directory_path)}")
    image_file_paths = [os.path.join(os.path.abspath(image_directory_path), file) for file in image_files]
    random.shuffle(image_file_paths)
    return image_file_paths


def resize_image_if_necessary(image_file_path):
    if os.path.getsize(image_file_path) > MAX_AVAILABLE_TELEGRAM_IMAGE_SIZE:
        image = Image.open(image_file_path)
        image.thumbnail(RESIZED_IMAGE_RESOLUTION, Image.Resampling.LANCZOS)
        with open(image_file_path, 'wb') as outfile:
            image.save(outfile, "JPEG")
            image.close()


def publish_images(publish_delay, image_file_paths, telegram_bot, telegram_chat_id):
    while image_file_paths:
        image_file_path = image_file_paths.pop()
        resize_image_if_necessary(image_file_path)
        upload_file_image(image_file_path, telegram_bot, telegram_chat_id)
        sleep(publish_delay)
        if not image_file_paths:
            image_file_paths = get_shuffled_image_paths(image_directory)


def upload_file_image(image_file_path, telegram_bot, telegram_chat_id):
    with open(image_file_path, 'rb') as f:
        telegram_bot.send_photo(chat_id=telegram_chat_id, photo=f)


def get_args():
    parser = argparse.ArgumentParser(
        prog="upload_images_to_telegram.py",
        description="Uploads local images to telegram channel"
    )
    parser.add_argument("--delay", help="publish delay in seconds", type=int, default=4 * 60 * 60)
    parser.add_argument("--image_directory", help="directory with images for upload", default="images")
    parser.add_argument("--image_file", help="image for publish")
    return parser.parse_args()


def main():
    load_dotenv()
    telegram_bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    telegram_chat_id = int(os.getenv("TELEGRAM_CHAT_ID"))
    args = get_args()
    if args.image_file:
        upload_file_image(args.image_file, telegram_bot, telegram_chat_id)
    else:
        image_file_paths = get_shuffled_image_paths(args.image_directory)
        publish_images(args.delay, image_file_paths, telegram_bot, telegram_chat_id)


if __name__ == '__main__':
    main()
