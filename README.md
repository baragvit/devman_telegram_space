## About The Project

Telegram space photo upload Devman learning project. Photos are downloaded from Space X and NASA resources to the project "images" directory.

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
```sh
python3 fetch_nasa_epic_images.py --image_directory images
python3 fetch_nasa_apod_images.py --image_directory images --image_count 5
python3 fetch_spacex_images.py --image_diretory images latest
```

## License
This project is licensed under the terms of the MIT license
