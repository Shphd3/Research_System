#!/usr/bin/env python3
"""Launch GPU processes on each ACP worker using an operator-provided rendezvous file."""

import argparse
from ipaddress import ip_address
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("endpoints", type=Path)
    parser.add_argument("--wait-seconds", type=int, default=300)
    parser.add_argument("--run-seconds", type=int, default=300)
    parser.add_argument("--port", type=int, default=29632)
    parser.add_argument("--nproc-per-node", type=int, default=1, help="Training processes per worker (default: 1)")
    parser.add_argument("--pod-ip", help="Explicit worker Pod IP if the auto check is ambiguous")
    parser.add_argument("training", type=Path)
    args, training_args = parser.parse_known_args()
    if min(args.wait_seconds, args.run_seconds) <= 0 or not 1024 <= args.port <= 65535:
        parser.error("Timeouts must be positive and port must be in 1024–65535")

    if args.nproc_per_node < 1:
        parser.error("Processes per node must be positive")

    deadline = time.monotonic() + args.wait_seconds
    while not args.endpoints.is_file():
        if time.monotonic() >= deadline:
            raise SystemExit("Rendezvous file did not arrive before the deadline")
        time.sleep(1)

    entries = json.loads(args.endpoints.read_text())
    addresses = [ip_address(entry) for entry in entries]
    if len(addresses) < 2 or len(set(addresses)) != len(addresses):
        raise SystemExit("Expected at least two distinct worker IPs")
    if any(ip.version != 4 or not ip.is_private or ip.is_loopback for ip in addresses):
        raise SystemExit("Expected private, non-loopback IPv4 Pod addresses")

    candidates = (
        {args.pod_ip}
        if args.pod_ip
        else set(subprocess.check_output(["hostname", "-I"], text=True, timeout=5).split())
    )
    matches = [rank for rank, addr in enumerate(addresses) if str(addr) in candidates]
    if len(matches) != 1:
        raise SystemExit("The worker must match exactly one IP in the rendezvous file")

    env = os.environ.copy()
    for name in ("MASTER_ADDR", "MASTER_PORT", "RANK", "WORLD_SIZE", "LOCAL_RANK",
                 "LOCAL_WORLD_SIZE", "GROUP_RANK"):
        env.pop(name, None)
    env.update(NCCL_DEBUG="INFO", NCCL_DEBUG_SUBSYS="INIT,NET,GRAPH")
    command = [
        sys.executable, "-m", "torch.distributed.run",
        f"--nnodes={len(addresses)}", f"--nproc-per-node={args.nproc_per_node}", "--max-restarts=0",
        f"--node-rank={matches[0]}", f"--master-addr={addresses[0]}",
        f"--master-port={args.port}", str(args.training), *training_args,
    ]
    try:
        return subprocess.run(command, env=env, timeout=args.run_seconds).returncode
    except subprocess.TimeoutExpired:
        print("Distributed worker exceeded the run timeout", file=sys.stderr)
        return 124


if __name__ == "__main__":
    raise SystemExit(main())
