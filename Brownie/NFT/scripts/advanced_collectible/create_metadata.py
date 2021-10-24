from brownie import accounts, network, config, AdvancedCollectible, LinkToken, VRFCoordinatorMock, Contract
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json

DOG_BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def upload_to_ipfs(filepath):
    # Reading Images as Binaries
    with Path(filepath).open("rb") as file_path:
        image_binary = file_path.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./images/0-pug.png" -> "0-pug.png"
        filename = filepath.split("/")[-1:][0]
        # "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        return image_uri


def main():
    # Getting the most recent deployed AdvancedCollectible
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    for token_id in range(number_of_advanced_collectibles):
        dog_breed_number = advanced_collectible.tokenIdToDogBreed(token_id)
        dog_breed = DOG_BREED_MAPPING[dog_breed_number]
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{dog_breed}.json"
        collectible_metadata = metadata_template
        # Checking if File exists
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata File: {metadata_file_name}")
            collectible_metadata["name"] = dog_breed
            collectible_metadata["description"] = f"An adorable {dog_breed} Pup"
            image_path = "./images/" + dog_breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image_uri"] = image_uri
            # Creating Metadata File
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            # Uploading Metadata File
            upload_to_ipfs(metadata_file_name)
