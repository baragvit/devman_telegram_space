import os
import random
import logging
from time import sleep

import telegram
from dotenv import load_dotenv

IMAGE_PUBLISH_DELAY_IN_SECONDS = 4 * 60 * 60

IMAGE_DIRECTORY_PATH = "images"


class ImagesNotExist(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_publish_delay():
    return int(os.getenv("IMAGE_PUBLISH_DELAY", IMAGE_PUBLISH_DELAY_IN_SECONDS))


def get_shuffled_image_paths():
    image_files = os.listdir(IMAGE_DIRECTORY_PATH)
    if len(image_files) == 0:
        raise ImagesNotExist(f"Files not found in {os.path.abspath(IMAGE_DIRECTORY_PATH)} directory")
    random.shuffle(image_files)
    return image_files


def main():
    load_dotenv()
    image_files = get_shuffled_image_paths()
    telegram_bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    telegram_chat_id = int(os.getenv("TELEGRAM_CHAT_ID"))
    while True:
        if len(image_files) == 0:
            image_files = get_shuffled_image_paths()
        image_file = image_files.pop()
        try:
            telegram_bot.send_photo(chat_id=telegram_chat_id,
                                    photo=open(os.path.join(IMAGE_DIRECTORY_PATH, image_file), 'rb'))
        except Exception as e:
            logging.error("Failed to upload photo", e)
        sleep(get_publish_delay())


if __name__ == '__main__':
    main()
