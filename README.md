## About The Project

Telegram space photo upload Devman learning project. Photos are downloaded from Space X and NASA resources to the project "images" directory. Images are uploaded to
telegram channel.

## Getting Started

### Prerequisites
Python3 interpreter version 3.12 and above, [venv](https://docs.python.org/3/library/venv.html)

### Installation
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
Credentials (NASA_TOKEN, TELEGRAM_BOT_TOKEN) should be provided to scripts as environment variables.  
Images downloading
```sh
NASA_TOKEN=provided_nasa_token python3 fetch_nasa_epic_images.py --image_directory images
NASA_TOKEN=provided_nasa_token python3 fetch_nasa_apod_images.py --image_directory images --image_count 5
python3 fetch_spacex_images.py --image_diretory images latest
```

Images uploading.
```sh
TELEGRAM_BOT_TOKEN=provided_bot_token TELEGRAM_CHAT_ID=provided_telegram_chat_id python3 upload_images_to_telegram.py
```
Optional publish delay in seconds env variable (IMAGE_PUBLISH_DELAY) can be provided to uploading script to override
default 4 hours delay.

## License
This project is licensed under the terms of the MIT license
