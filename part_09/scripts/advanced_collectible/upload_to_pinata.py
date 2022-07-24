import os
from pathlib import Path
import requests

PINATA_BASE_URL: str = "https://api.pinata.cloud/"
endpoint: str = "pinning/pinFileToIPFS"
filepath: str = "./img/pug.png"
filename: str = filepath.split("/")[-1:][0]
headers: dict = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_KEY"),
}


def main():
    with Path(filepath).open("rb") as f:
        image_binary = f.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())
