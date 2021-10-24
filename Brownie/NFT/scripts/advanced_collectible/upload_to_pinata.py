import os
from pathlib import Path
import requests


def main():
    filepath = "./images/pug.png"
    # "./images/0-pug.png" -> "0-pug.png"
    file_name = filepath.split("/")[-1:][0]
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET")
    }
    with Path(filepath).open("rb") as file_path:
        image_binary = file_path.read()
        pinata_base_url = "https://api.pinata.cloud"
        endpoint = "pinning/pinFileToIPFS"
        response = requests.post(
            pinata_base_url + endpoint,
            files={"file": (file_name, image_binary)},
            headers=headers
        )
