#!/usr/bin/env python3
"""
Entry point for the Binance Futures Testnet Trading Bot.
"""
import sys

# Optional: suppress standard traceback printing to console if uncaught exception happens
# We handle most exceptions in cli.py, but this ensures a clean UX if something extremely weird happens.
sys.tracebacklimit = 0

from bot.cli import app

if __name__ == "__main__":
    app()
