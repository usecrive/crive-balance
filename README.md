# CRIVE Balance

Local Python CLI to read native and ERC-20 balances on **Robinhood Chain** for addresses you supply.

**Language:** Python 3  
**Scope:** Client-side / local only  
**Credentials:** None — public RPC only  
**Project:** [CRIVE](https://usecrive.com) · [github.com/usecrive](https://github.com/usecrive)

## What it does

- Queries native balance (`eth_getBalance`)
- Optionally queries ERC-20 `balanceOf` via `eth_call`
- Prints human-readable amounts using the token decimals you pass

## Requirements

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` is intentionally empty of heavy SDKs — only the standard library is required. Optional: none.

## Usage

```bash
# Native balance
python -m crive_balance 0xYourAddressHere

# ERC-20 balance (token, holder, decimals)
python -m crive_balance 0xHolder --token 0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168 --decimals 6

# Custom public RPC
python -m crive_balance 0xYourAddressHere --rpc https://rpc.mainnet.chain.robinhood.com
```

## Defaults

| Setting | Value |
|---------|--------|
| Chain | Robinhood Chain (4663) |
| RPC | `https://rpc.mainnet.chain.robinhood.com` |
| Example USDG | `0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168` (6 decimals) |

## Safety

- Read-only RPC (`eth_getBalance`, `eth_call`)
- Never asks for private keys or mnemonics
- Does not write transactions

## License

MIT
