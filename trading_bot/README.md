# Binance Futures Testnet Trading Bot

A production-quality Python CLI application for placing MARKET and LIMIT orders on the Binance Futures Testnet (USDT-M). Designed with clean architecture, robust validation, and a professional user experience.

## Architecture & Design Choices

The project is structured to reflect professional backend engineering standards:

*   **Modular Design**: Logic is strictly separated into focused modules (`config.py`, `validators.py`, `client.py`, `orders.py`, `cli.py`). This prevents "god classes" or giant scripts.
*   **Rich CLI (Typer & Rich)**: Instead of messy `print()` statements, the app provides a highly readable, colored, and formatted terminal UX.
*   **Centralized Configuration**: `dotenv` is used to inject secrets safely. No hardcoded API keys exist in the codebase.
*   **Robust Logging**: A rotating file logger captures all lifecycle events, requests, and validation failures without polluting the terminal UI.
*   **Graceful Error Handling**: The bot catches network errors, Binance API exceptions (e.g., precision errors, insufficient margin), and validation failures, translating them into human-readable panels. It avoids ugly stack traces for standard user errors.

## Project Structure

```
trading_bot/
│
├── bot/
│   ├── __init__.py       # Package marker
│   ├── client.py         # Binance Client initialization
│   ├── orders.py         # Market and Limit order execution logic
│   ├── validators.py     # Input sanitization and validation
│   ├── logging_config.py # Rotating file logger setup
│   ├── config.py         # Environment variables and constants
│   └── cli.py            # Typer application and Rich UI formatting
│
├── logs/
│   └── trading.log       # Application logs (auto-generated)
│
├── .env.example          # Template for environment variables
├── requirements.txt      # Project dependencies
└── main.py               # Application entry point
```

## Setup & Installation

### 1. Prerequisites
*   Python 3.8+
*   A Binance Futures Testnet account (https://testnet.binancefuture.com/en/login)

### 2. Virtual Environment Setup
It's highly recommended to use a virtual environment.

```bash
# Create the virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
1.  Copy the `.env.example` file to `.env`:
    ```bash
    cp .env.example .env
    ```
2.  Open `.env` and fill in your Binance Testnet API keys:
    ```env
    BINANCE_API_KEY=your_testnet_api_key
    BINANCE_API_SECRET=your_testnet_api_secret
    LOG_LEVEL=INFO
    ```

## Usage

The CLI accepts several arguments to place trades.

```bash
python main.py trade --help
```

### MARKET Order Example
Places a market order. Price is ignored if provided.

```bash
python main.py trade --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### LIMIT Order Example
Places a limit order (GTC - Good Till Cancelled). Requires a price.

```bash
python main.py trade --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 3500.0
```

## Assumptions
*   **Trading Pair**: The bot expects standard Binance Futures symbols (e.g., `BTCUSDT`).
*   **Network Stability**: The bot assumes a stable connection, but traps `requests.exceptions.RequestException` to handle unexpected drops gracefully.
*   **Time In Force**: LIMIT orders default to `GTC` (Good Till Cancelled).

## Troubleshooting

*   **APIError(code=-2015): Invalid API-key, IP, or permissions for action.**
    Ensure you are using keys generated from the *Testnet*, not your live Binance account.
*   **APIError(code=-1111): Precision is over the maximum defined for this asset.**
    You are trying to order a quantity or price with too many decimal places for the given symbol.
*   **Network Error Panel**
    Check your internet connection or verify that the Binance Testnet API is currently online. Check `logs/trading.log` for full stack traces.
