import json

from web3 import Web3

from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()

SOLC_VERSION: str = "0.6.0"
HTTP_PROVIDER_ADDR: str = "http://127.0.0.1:7545"
CHAIN_ID: int = 1337
PUB_KEY: str = "0x9bd6fc6264a14423A762bB206E9442f775571E16"
PRIV_KEY: str = "0x8ffa2e4643ab7bb4afa8853829179911ad73624b16cca707b4032e72733d7d2d"

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
        }
    },
    solc_version=SOLC_VERSION,
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get the bytecode from the JSON with the compiled code file
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get ABI
abi = json.loads(compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"])["output"]["abi"]

w3: Web3 = Web3(Web3.HTTPProvider(HTTP_PROVIDER_ADDR))
chain_id: int = CHAIN_ID
my_addr: str = PUB_KEY
private_key: str =  PRIV_KEY

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
