import os


def get_nasa_api_token():
    nasa_api_token = os.getenv("NASA_TOKEN")
    if not nasa_api_token:
        raise NasaApiTokenNotFoundException("Api token should be provided as environment variable NASA_TOKEN")
    return nasa_api_token


class NasaApiTokenNotFoundException(Exception):
    pass
