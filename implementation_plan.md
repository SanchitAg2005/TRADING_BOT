# Binance Futures CLI Trading Bot Implementation Plan

This plan details the implementation of a production-quality Python CLI trading bot for Binance Futures Testnet, following the exact structure and requirements provided.

## User Review Required

Please review the proposed structure and the libraries we will use. I've selected the following dependencies as per your request:
- `python-binance` (Official or community standard for Binance API)
- `typer` (For building the CLI interface)
- `rich` (For beautiful terminal outputs and tables)
- `python-dotenv` (For environment variable management)

Are there any other specific constraints (e.g., specific versions) you'd like to enforce for the dependencies?

## Proposed Changes

We will build the application in a new `trading_bot` directory within your workspace.

### Core Configuration and Setup

#### [NEW] [requirements.txt](file:///c:/Users/agarw/Downloads/internship/trading_bot/requirements.txt)
Dependencies for the project.

#### [NEW] [.env.example](file:///c:/Users/agarw/Downloads/internship/trading_bot/.env.example)
Template for API keys.

#### [NEW] [.gitignore](file:///c:/Users/agarw/Downloads/internship/trading_bot/.gitignore)
Standard Python gitignore, ensuring `.env` is ignored.

#### [NEW] [main.py](file:///c:/Users/agarw/Downloads/internship/trading_bot/main.py)
A small entry point script that simply invokes the Typer CLI app.

---

### Bot Package

#### [NEW] [__init__.py](file:///c:/Users/agarw/Downloads/internship/trading_bot/bot/__init__.py)
Package marker.

#### [NEW] [config.py](file:///c:/Users/agarw/Downloads/internship/trading_bot/bot/config.py)
Loads environment variables using `dotenv` and exposes them as typed constants. It handles missing API keys gracefully.

#### [NEW] [logging_config.py](file:///c:/Users/agarw/Downloads/internship/trading_bot/bot/logging_config.py)
Sets up the standard Python `logging` module to output formatted logs to `logs/trading.log`. It will include timestamps, log levels, and messages.

#### [NEW] [validators.py](file:///c:/Users/agarw/Downloads/internship/trading_bot/bot/validators.py)
Contains validation logic for:
- Symbols (e.g., must end with USDT, alphanumeric)
- Quantity (must be strictly > 0)
- Order types and sides
- Price requirements for limit orders

#### [NEW] [client.py](file:///c:/Users/agarw/Downloads/internship/trading_bot/bot/client.py)
Initializes the `Client` from `python-binance`. It configures the client to connect specifically to the Futures Testnet (`testnet=True` or explicitly overriding the API URL). It wraps basic API error handling.

#### [NEW] [orders.py](file:///c:/Users/agarw/Downloads/internship/trading_bot/bot/orders.py)
Contains functions `place_market_order` and `place_limit_order`. This module communicates with the client and returns clean dictionaries/dataclasses or handles the `BinanceAPIException`.

#### [NEW] [cli.py](file:///c:/Users/agarw/Downloads/internship/trading_bot/bot/cli.py)
The `typer` interface. It will expose a command (e.g., `trade`) accepting all required arguments, call validators, execute orders, and use `rich` panels/tables to output the result professionally.

---

### Documentation and Logs

#### [NEW] [README.md](file:///c:/Users/agarw/Downloads/internship/trading_bot/README.md)
A comprehensive, recruiter-friendly documentation explaining how to setup, configure, and use the bot.

#### [NEW] [trading.log](file:///c:/Users/agarw/Downloads/internship/trading_bot/logs/trading.log)
Example logs populated with realistic MARKET and LIMIT order transactions.

## Verification Plan

### Manual Verification
1. Create a `trading_bot/.env` file with dummy or real Testnet keys.
2. Run validation checks to ensure proper error messages:
   - `python main.py --symbol btc --side BUY --type MARKET --quantity 0`
   - `python main.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 1` (missing price)
3. Run a valid MARKET order: `python main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001`
4. Run a valid LIMIT order: `python main.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 90000`
5. Check `logs/trading.log` to verify logging formatting.
6. Observe terminal output to ensure `rich` UI elements (tables/panels) are rendering correctly.
