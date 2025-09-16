#!/usr/bin/env python3
"""
Mock CLI application for testing purposes.
This is a minimal implementation to satisfy test imports.
"""

import typer
from typing import Optional

app = typer.Typer()

@app.command()
def reveal(prospect_id: str):
    """Mock reveal command for testing."""
    print(f"Revealing prospect: {prospect_id}")

@app.command()
def main():
    """Main CLI entry point."""
    pass

if __name__ == "__main__":
    app()