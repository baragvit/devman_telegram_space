import os
import random

import telegram
from dotenv import load_dotenv

TELEGRAM_CHAT_ID = -4706551698

IMAGE_DIRECTORY_PATH = "images"


def main():
    load_dotenv()
    image_files = os.listdir(IMAGE_DIRECTORY_PATH)
    image_file = random.choice(image_files)
    bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
    bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(os.path.join(IMAGE_DIRECTORY_PATH, image_file), 'rb'))


if __name__ == '__main__':
    main()
