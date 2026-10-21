"""CRIVE Balance — local balance reader for Robinhood Chain (public RPC)."""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request

DEFAULT_RPC = "https://rpc.mainnet.chain.robinhood.com"
CHAIN_ID = 4663


def rpc_call(rpc: str, method: str, params: list) -> object:
    body = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    ).encode()
    req = urllib.request.Request(
        rpc,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode())
    if "error" in data:
        raise RuntimeError(data["error"])
    return data.get("result")


def format_units(raw: int, decimals: int) -> str:
    if decimals == 0:
        return str(raw)
    s = str(raw).zfill(decimals + 1)
    whole, frac = s[:-decimals], s[-decimals:]
    frac = frac.rstrip("0") or "0"
    return f"{whole}.{frac}"


def main() -> int:
    p = argparse.ArgumentParser(description="CRIVE Balance — Robinhood Chain")
    p.add_argument("address", help="Wallet address (0x…)")
    p.add_argument("--token", help="ERC-20 contract address", default=None)
    p.add_argument("--decimals", type=int, default=18)
    p.add_argument("--rpc", default=DEFAULT_RPC)
    args = p.parse_args()

    addr = args.address.strip().lower()
    if not addr.startswith("0x") or len(addr) != 42:
        print("Invalid address", file=sys.stderr)
        return 1

    print(f"CRIVE Balance · chain {CHAIN_ID}")
    print(f"RPC: {args.rpc}")
    print(f"Address: {addr}")

    if args.token:
        token = args.token.strip().lower()
        # balanceOf(address) selector 0x70a08231 + padded address
        data = "0x70a08231" + addr[2:].rjust(64, "0")
        result = rpc_call(args.rpc, "eth_call", [{"to": token, "data": data}, "latest"])
        raw = int(result, 16)
        print(f"Token: {token}")
        print(f"Balance: {format_units(raw, args.decimals)} (raw {raw})")
    else:
        result = rpc_call(args.rpc, "eth_getBalance", [addr, "latest"])
        raw = int(result, 16)
        print(f"Native: {format_units(raw, 18)} ETH (raw {raw})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
