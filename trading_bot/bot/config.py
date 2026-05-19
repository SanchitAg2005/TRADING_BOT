import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration for the trading bot."""
    
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")
    
    # Futures Testnet Base URL
    BINANCE_FUTURES_TESTNET_URL = "https://testnet.binancefuture.com"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "trading.log")

    @classmethod
    def validate(cls):
        """Validate that all required configuration is present."""
        if not cls.BINANCE_API_KEY or not cls.BINANCE_API_SECRET:
            raise ValueError(
                "Missing Binance API credentials. "
                "Please ensure BINANCE_API_KEY and BINANCE_API_SECRET are set in the .env file."
            )

config = Config()
