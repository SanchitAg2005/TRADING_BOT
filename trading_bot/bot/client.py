from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .config import config
from .logging_config import logger

def get_client() -> Client:
    """
    Initializes and returns the Binance Client configured for Futures Testnet.
    """
    try:
        config.validate()
        
        # Initialize client with testnet=True which handles Testnet routing
        client = Client(
            api_key=config.BINANCE_API_KEY,
            api_secret=config.BINANCE_API_SECRET,
            testnet=True
        )
        
        # Force the Futures URL to the Testnet URL just to be absolutely safe
        client.FUTURES_URL = config.BINANCE_FUTURES_TESTNET_URL + "/fapi"
        
        return client
        
    except ValueError as e:
        logger.error(f"Configuration Error: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to initialize Binance Client: {e}", exc_info=True)
        raise
