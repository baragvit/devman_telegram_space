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
Credentials ([NASA_TOKEN](https://api.nasa.gov/), [TELEGRAM_BOT_TOKEN](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)) and TELEGRAM_CHAT_ID should be provided to scripts as environment variables.

### Images downloading
```sh
NASA_TOKEN=provided_nasa_token python3 fetch_nasa_epic_images.py --image_directory images
NASA_TOKEN=provided_nasa_token python3 fetch_nasa_apod_images.py --image_directory images --image_count 5
python3 fetch_spacex_images.py --image_directory images latest
```

### Images uploading
Uploading single image file
```sh
TELEGRAM_BOT_TOKEN=provided_bot_token TELEGRAM_CHAT_ID=provided_telegram_chat_id python3 upload_images_to_telegram.py --image_file path_to_file
```

Uploading shuffled files from directory with custrom delay in seconds
```sh
TELEGRAM_BOT_TOKEN=provided_bot_token TELEGRAM_CHAT_ID=provided_telegram_chat_id python3 upload_images_to_telegram.py --delay 5000 --image_directory images
```

## License
This project is licensed under the terms of the MIT license
