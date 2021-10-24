from brownie import accounts, network, config, AdvancedCollecitble

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "mainnet-fork"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
DOG_BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}
dog_metadata_dictionary = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def main():
    print(f"Working on Network {network.show_active()}")
    # Recent deployed AdvancedCollectible
    advanced_collectible = AdvancedCollecitble[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"{number_of_collectibles} Token Ids exists")
    for token_id in range(number_of_collectibles):
        dog_breed_number = advanced_collectible.tokenIdToDogBreed(token_id)
        dog_breed = DOG_BREED_MAPPING[dog_breed_number]
        # NFT does not have been set
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting Toke URI of {token_id}")
            # Setting Token URI
            account = get_account()
            # Instead of using a Dictionary the Token URI could be graped from the JSON Files
            setting_transaction = advanced_collectible.setTokenURI(token_id, dog_metadata_dictionary[dog_breed], {"account": account})
            setting_transaction.wait(1)
            print(f"NFT at {OPENSEA_URL.format(advanced_collectible.address, token_id)}")
