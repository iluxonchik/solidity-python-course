from brownie import AdvancedCollectible, network
from scripts.utils import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json


def create_metadata():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles: int = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles")
    for token_id in range(number_of_advanced_collectibles):
        breed: str = get_breed(advanced_collectible.tokenIdToBreed(token_id))

        metadata_file_name: str = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        print(f"{metadata_file_name=}")

        collectible_metadata: dict = metadata_template.copy()
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name=} alrady exists. Delete it to override")
        else:
            print(f"Creating {metadata_file_name=}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"A pimperish {breed} dawg"

            image_path: str = f"./img/{breed.lower().replace('_', '-')}.png"
            image_uri: str = upload_to_ipfs(image_path)

            collectible_metadata["image_uri"] = image_uri
            with open(metadata_file_name, "w") as f:
                json.dump(collectible_metadata, f)
            upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath) -> str:
    IPFS_URL: str = "http://127.0.0.1:5001"
    with Path(filepath).open("rb") as f:
        image_binary = f.read()
        endpoint: str = "/api/v0/add"
        response = requests.post(f"{IPFS_URL}{endpoint}", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # transform "./img/0-PUG.png" to "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        image_uri: str = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri


def main():
    create_metadata()
