#!/usr/bin/env python3
"""
Demo CLI for agentic, JSON-first commands.

Usage examples:
  python demo_cli.py sum --a 2 --b 3 --format json
  python demo_cli.py echo --message "hello" --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict


@dataclass
class Response:
    ok: bool
    code: str
    data: dict
    message: str = ""
    version: str = "1"

    def to_json(self) -> str:
        return json.dumps(asdict(self), separators=(",", ":"), sort_keys=True)


def cmd_sum(args: argparse.Namespace) -> int:
    total = args.a + args.b
    resp = Response(ok=True, code="SUM_OK", data={"a": args.a, "b": args.b, "sum": total})
    if args.format == "json":
        print(resp.to_json())
    else:
        print(f"sum={total}")
    return 0


def cmd_echo(args: argparse.Namespace) -> int:
    resp = Response(ok=True, code="ECHO_OK", data={"message": args.message})
    if args.format == "json":
        print(resp.to_json())
    else:
        print(args.message)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="demo-cli", description="Demo agentic CLI (JSON-first)")
    sub = p.add_subparsers(dest="command", required=True)

    psum = sub.add_parser("sum", help="Add two integers")
    psum.add_argument("--a", type=int, required=True)
    psum.add_argument("--b", type=int, required=True)
    psum.add_argument("--format", choices=["json", "text"], default="json")
    psum.set_defaults(func=cmd_sum)

    pe = sub.add_parser("echo", help="Echo a message")
    pe.add_argument("--message", type=str, required=True)
    pe.add_argument("--format", choices=["json", "text"], default="json")
    pe.set_defaults(func=cmd_echo)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as e:  # deterministic error surface
        err = Response(ok=False, code="ERR", data={}, message=str(e))
        print(err.to_json(), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

