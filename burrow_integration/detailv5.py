#detailv3.py
#best version so far

from Crypto.Hash import keccak
import os
import binascii
from iroha import IrohaCrypto
from iroha import Iroha, IrohaGrpc
from iroha.ed25519 import H
import integration_helpers
import csv
from iroha.primitive_pb2 import can_set_my_account_detail
import sys
from icecream import ic


if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

IROHA_HOST_ADDR = os.getenv("IROHA_HOST_ADDR", "127.0.0.1")
IROHA_PORT = os.getenv("IROHA_PORT", "50051")
ADMIN_ACCOUNT_ID = os.getenv("ADMIN_ACCOUNT_ID", "admin@test")
ADMIN_PRIVATE_KEY = os.getenv(
    "ADMIN_PRIVATE_KEY",
    "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70",
)

user_private_key = IrohaCrypto.private_key()
user_public_key = IrohaCrypto.derive_public_key(user_private_key)
iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc("{}:{}".format(IROHA_HOST_ADDR, IROHA_PORT))

# Read account attributes from a csv
def read_accounts_from_csv(file_path):
    accounts = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            accounts.append({
                'account_id': row['Account ID']
            })
    return accounts


# Path to the CSV file
csv_file_path = 'accounts1.csv'

# Read accounts from CSV
accounts = read_accounts_from_csv(csv_file_path)

# Use the [n] account from the CSV for the example
account = accounts[5]



@integration_helpers.trace
def create_contract():
    bytecode = "608060405234801561001057600080fd5b5073a6abc17819738299b3b2c1ce46d55c74f04e290c6000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550610b4c806100746000396000f3fe608060405234801561001057600080fd5b506004361061004c5760003560e01c80635bdb3a41146100515780637949a1b31461006f578063b7d66df71461009f578063d4e804ab146100cf575b600080fd5b6100596100ed565b6040516100669190610879565b60405180910390f35b61008960048036038101906100849190610627565b61024c565b6040516100969190610879565b60405180910390f35b6100b960048036038101906100b49190610693565b6103bb565b6040516100c69190610879565b60405180910390f35b6100d761059b565b6040516100e4919061085e565b60405180910390f35b606060006040516024016040516020818303038152906040527f5bdb3a41000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff8381831617835250505050905060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16836040516101be9190610830565b600060405180830381855af49150503d80600081146101f9576040519150601f19603f3d011682016040523d82523d6000602084013e6101fe565b606091505b509150915081610243576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161023a9061091e565b60405180910390fd5b80935050505090565b60606000838360405160240161026392919061089b565b6040516020818303038152906040527f7949a1b3000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff8381831617835250505050905060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168360405161032a9190610830565b600060405180830381855af49150503d8060008114610365576040519150601f19603f3d011682016040523d82523d6000602084013e61036a565b606091505b5091509150816103af576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016103a69061091e565b60405180910390fd5b80935050505092915050565b606060008484846040516024016103d4939291906108d2565b6040516020818303038152906040527fb7d66df7000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff8381831617835250505050905060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168360405161049b9190610830565b600060405180830381855af49150503d80600081146104d6576040519150601f19603f3d011682016040523d82523d6000602084013e6104db565b606091505b509150915081610520576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016105179061091e565b60405180910390fd5b8460405161052e9190610847565b6040518091039020866040516105449190610847565b60405180910390208860405161055a9190610847565b60405180910390207f5e1b38cd47cf21b75d5051af29fa321eedd94877db5ac62067a076770eddc9d060405160405180910390a48093505050509392505050565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60006105d26105cd84610963565b61093e565b9050828152602081018484840111156105ea57600080fd5b6105f5848285610a14565b509392505050565b600082601f83011261060e57600080fd5b813561061e8482602086016105bf565b91505092915050565b6000806040838503121561063a57600080fd5b600083013567ffffffffffffffff81111561065457600080fd5b610660858286016105fd565b925050602083013567ffffffffffffffff81111561067d57600080fd5b610689858286016105fd565b9150509250929050565b6000806000606084860312156106a857600080fd5b600084013567ffffffffffffffff8111156106c257600080fd5b6106ce868287016105fd565b935050602084013567ffffffffffffffff8111156106eb57600080fd5b6106f7868287016105fd565b925050604084013567ffffffffffffffff81111561071457600080fd5b610720868287016105fd565b9150509250925092565b610733816109e2565b82525050565b600061074482610994565b61074e81856109aa565b935061075e818560208601610a23565b61076781610ab6565b840191505092915050565b600061077d82610994565b61078781856109bb565b9350610797818560208601610a23565b80840191505092915050565b60006107ae8261099f565b6107b881856109c6565b93506107c8818560208601610a23565b6107d181610ab6565b840191505092915050565b60006107e78261099f565b6107f181856109d7565b9350610801818560208601610a23565b80840191505092915050565b600061081a6027836109c6565b915061082582610ac7565b604082019050919050565b600061083c8284610772565b915081905092915050565b600061085382846107dc565b915081905092915050565b6000602082019050610873600083018461072a565b92915050565b600060208201905081810360008301526108938184610739565b905092915050565b600060408201905081810360008301526108b581856107a3565b905081810360208301526108c981846107a3565b90509392505050565b600060608201905081810360008301526108ec81866107a3565b9050818103602083015261090081856107a3565b9050818103604083015261091481846107a3565b9050949350505050565b600060208201905081810360008301526109378161080d565b9050919050565b6000610948610959565b90506109548282610a56565b919050565b6000604051905090565b600067ffffffffffffffff82111561097e5761097d610a87565b5b61098782610ab6565b9050602081019050919050565b600081519050919050565b600081519050919050565b600082825260208201905092915050565b600081905092915050565b600082825260208201905092915050565b600081905092915050565b60006109ed826109f4565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b82818337600083830152505050565b60005b83811015610a41578082015181840152602081019050610a26565b83811115610a50576000848401525b50505050565b610a5f82610ab6565b810181811067ffffffffffffffff82111715610a7e57610a7d610a87565b5b80604052505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6000601f19601f8301169050919050565b7f4572726f722063616c6c696e67207365727669636520636f6e7472616374206660008201527f756e6374696f6e0000000000000000000000000000000000000000000000000060208201525056fea26469706673582212206ad40afbd4cc9c87ae154542d003c9538e4b89473a13cadd3cbf618ea181206864736f6c63430008040033"
    """Bytecode was generated using remix editor  https://remix.ethereum.org/ from file detail.sol. """
    tx = iroha.transaction(
        [iroha.command("CallEngine", caller=ADMIN_ACCOUNT_ID, input=bytecode)]
    )
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    net.send_tx(tx)
    hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
    for status in net.tx_status_stream(tx):
        ic(status)
    return hex_hash


@integration_helpers.trace
def set_account_detail(address, account):
    params = integration_helpers.get_first_four_bytes_of_keccak(
        b"setAccountDetail(string,string,string)"
    )
    no_of_param = 3
    for x in range(no_of_param):
        params = params + integration_helpers.left_padded_address_of_param(
            x, no_of_param
        )
    params = params + integration_helpers.argument_encoding(
        account['account_id']
    )  # source account id
    params = params + integration_helpers.argument_encoding("duper")  # key
    params = params + integration_helpers.argument_encoding("NAOEHOADMIN019050919050565b600081519050919050565b600081519050919050565b600082825260208201905092915050565b600081905092915050565b60008")  #  value
    tx = iroha.transaction(
        [
            iroha.command(
                "CallEngine", caller=ADMIN_ACCOUNT_ID, callee=address, input=params
            )
        ]
    )
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    response = net.send_tx(tx)
    ic(response)
    for status in net.tx_status_stream(tx):
        ic(status)
    hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
    return hex_hash


@integration_helpers.trace
def get_account_details():
    params = integration_helpers.get_first_four_bytes_of_keccak(b"getAccountDetail()")
    no_of_param = 0
    tx = iroha.transaction(
        [
            iroha.command(
                "CallEngine", caller=ADMIN_ACCOUNT_ID, callee=address, input=params
            )
        ]
    )
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    response = net.send_tx(tx)
    for status in net.tx_status_stream(tx):
        ic(status)
    hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
    return hex_hash


hash = create_contract()
ic(hash)
address = integration_helpers.get_engine_receipts_address(hash)
ic(address)
hash = get_account_details()
integration_helpers.get_engine_receipts_result(hash)
hash = set_account_detail(address, account)
ic(account)
hash = get_account_details()
integration_helpers.get_engine_receipts_result(hash)
ic("done")
