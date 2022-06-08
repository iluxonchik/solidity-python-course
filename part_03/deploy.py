import json

from web3 import Web3

from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()

SOLC_VERSION: str = "0.6.0"
HTTP_PROVIDER_ADDR: str = "http://127.0.0.1:8545"
CHAIN_ID: int = 1337
PUB_KEY: str = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
PRIV_KEY: str = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

print("Installing...")
install_solc(SOLC_VERSION)

# compile the Solidity code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version=SOLC_VERSION,
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get the bytecode from the JSON with the compiled code file
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get ABI
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

w3: Web3 = Web3(Web3.HTTPProvider(HTTP_PROVIDER_ADDR))
chain_id: int = CHAIN_ID
my_addr: str = PUB_KEY
private_key: str = PRIV_KEY

# create the smart contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# get number of transaction for address
nonce: int = w3.eth.get_transaction_count(my_addr)
# build the transaction that contains the contract deployment
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_addr,
        "nonce": nonce,
    }
)
# sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract...")
# send the signed tranasaction contatining the contract deployment to the blockchain
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# wait for the transaction to be mined and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Contract successfully deployed to {tx_receipt.contractAddress}")

## Now let's invoke a contract
# When working with a contract, you always need 2 things:
# * the address of the contract
# * the contract's ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# 2 ways in which we can interact with a contract's functions:
# * call --> Simulate making a call to get a value back. this is read-only and it doesn't make a change to the state of the blockchain
# * transact --> actually mke a state change on the blockchain. you can always attempt to transact on a function, even if it's a views

# initial value of the favorite number
print(simple_storage.functions.retrieve().call())

# this won't update the value of the stored number, because it's a "call" on the function
print(f"**calling** sotre: {simple_storage.functions.store(15).call()}")
print(
    f"read retrieve after a **call** on the store(): {simple_storage.functions.retrieve().call()}"
)

# update the value of the stored number
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_addr,
        "nonce": w3.eth.get_transaction_count(my_addr),
        "gasPrice": w3.eth.gas_price,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

# get the updated value
print(simple_storage.functions.retrieve().call())
