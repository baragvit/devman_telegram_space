import argparse
import logging
import os
import random
import sys
import tempfile
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
    if len(image_files) == 0:
        raise ImagesNotExist(f"Files not found in {os.path.abspath(image_directory_path)} directory")
    image_file_paths = [os.path.join(os.path.abspath(image_directory_path), file) for file in image_files]
    random.shuffle(image_file_paths)
    return image_file_paths


def get_resized_file_descriptor(image_file_path):
    if os.path.getsize(image_file_path) < MAX_AVAILABLE_TELEGRAM_IMAGE_SIZE:
        return open(image_file_path, 'rb')
    im = Image.open(image_file_path)
    outfile = tempfile.TemporaryFile()
    im.thumbnail(RESIZED_IMAGE_RESOLUTION, Image.Resampling.LANCZOS)
    im.save(outfile, "JPEG")
    outfile.seek(0)
    return outfile


def publish_images(publish_delay, image_directory, telegram_bot, telegram_chat_id):
    image_file_paths = get_shuffled_image_paths(image_directory)
    if len(image_file_paths) == 0:
        sys.exit("no images to publish")
    while True:
        image_file_path = image_file_paths.pop()
        if len(image_file_paths) == 0:
            image_file_paths = get_shuffled_image_paths()
        try:
            upload_file_image(image_file_path, telegram_bot, telegram_chat_id)
        except Exception as e:
            logging.error("Failed to upload photo", e)
        sleep(publish_delay)


def upload_file_image(image_file_path, telegram_bot, telegram_chat_id):
    with get_resized_file_descriptor(image_file_path) as file_descriptor:
        telegram_bot.send_photo(chat_id=telegram_chat_id,
                                photo=file_descriptor)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--delay", help="publish delay in secdonds", type=int, default=4 * 60 * 60)
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
        publish_images(args.delay, args.image_directory, telegram_bot, telegram_chat_id)


if __name__ == '__main__':
    main()
