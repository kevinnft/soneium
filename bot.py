import asyncio
import random
import time
from web3 import Web3
from eth_account import Account
from colorama import Fore, Style, init

# Init colorama
init(autoreset=True)

# RPC & Chain
RPC_URL = "https://rpc.soneium.org"
CHAIN_ID = 1868
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# ERC20 ABI standar
ERC20_ABI = '''
[
    {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},
    {"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
    {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"}
]
'''

# Daftar token urut (bergantian)
TOKENS = [
    ("usd0", "0x102d758f688a4c1c5a80b116bd945d4455460282"),
    ("usdt", "0xba9986d2381edf1da03b0b9c1f8b00dc4aacc369"),
    ("usdc", "0x3a337a6ada9d885b6ad95ec48f9b75f197b5ae35"),
]

# Load wallets & target addresses
with open("wallets.txt") as f:
    PRIVATE_KEYS = [line.strip() for line in f if line.strip()]

with open("addres.txt") as f:
    TARGET_ADDRS = [line.strip() for line in f if line.strip()]

async def send_tokens():
    token_index = 0
    while True:
        for pk in PRIVATE_KEYS:
            acct = Account.from_key(pk)
            sender = acct.address

            # Ambil token sesuai urutan
            token_symbol, token_addr = TOKENS[token_index]
            contract = w3.eth.contract(address=Web3.to_checksum_address(token_addr), abi=ERC20_ABI)

            # Pilih target random
            target = Web3.to_checksum_address(random.choice(TARGET_ADDRS))

            try:
                decimals = contract.functions.decimals().call()

                # Random amount antara 0.000001 - 0.00001
                send_amount = random.uniform(0.000001, 0.00001)
                amount = int(send_amount * 10**decimals)

                balance_before = contract.functions.balanceOf(sender).call()

                if balance_before < amount:
                    print(Fore.YELLOW + f"[{sender[:6]}...] SKIP {token_symbol.upper()} | saldo: {balance_before/10**decimals:.6f}")
                else:
                    nonce = w3.eth.get_transaction_count(sender)
                    tx = contract.functions.transfer(target, amount).build_transaction({
                        'from': sender,
                        'nonce': nonce,
                        'chainId': CHAIN_ID,
                        'gas': 100000,
                        'gasPrice': w3.eth.gas_price
                    })

                    signed = w3.eth.account.sign_transaction(tx, private_key=pk)
                    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

                    balance_after = contract.functions.balanceOf(sender).call()

                    print(
                        Fore.GREEN
                        + f"[{sender[:6]}...] Sent {send_amount:.8f} {token_symbol.upper()} -> {target}\n"
                        + Fore.CYAN
                        + f"   Nonce: {nonce} | Tx: {w3.to_hex(tx_hash)}\n"
                        + Fore.MAGENTA
                        + f"   Sisa saldo: {balance_after/10**decimals:.6f} {token_symbol.upper()}"
                    )

            except Exception as e:
                print(Fore.RED + f"[{sender[:6]}...] ERROR: {str(e)}")

            # Geser token index (0 -> 1 -> 2 -> balik 0 lagi)
            token_index = (token_index + 1) % len(TOKENS)

            # Tunggu 5 menit (300 detik)
            time.sleep(300)

asyncio.run(send_tokens())
