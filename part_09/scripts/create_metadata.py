from brownie import AdvancedCollectible, network
from scripts.utils import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path


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
            image_uri = upload_to_ipfs()
            collectible_metadata["image_uri"] = image_uri


def upload_to_ipfs(filepath):
    # TODO
    pass


def main():
    create_metadata()
