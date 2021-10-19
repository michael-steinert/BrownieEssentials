from brownie import accounts, config, SimpleStorage

def read_contract():
    # Index have to be one less then the Length
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieveFavoriteNumber())

def main():
    read_contract()