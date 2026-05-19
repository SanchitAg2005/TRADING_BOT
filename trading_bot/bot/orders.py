from typing import Dict, Any, Optional
from binance.client import Client
from binance.exceptions import BinanceAPIException
from .logging_config import logger
from .client import get_client

def place_market_order(
    symbol: str, 
    side: str, 
    quantity: float
) -> Dict[str, Any]:
    """
    Places a MARKET order on Binance Futures Testnet.
    """
    logger.info(f"Preparing MARKET {side} order for {quantity} {symbol}")
    client = get_client()
    
    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        
        # If response shows NEW and orderId exists, fetch the updated order state
        # to get actual execution details (MARKET orders fill almost instantly)
        if response.get('status') == 'NEW' and response.get('orderId'):
            import time
            time.sleep(0.5)
            try:
                updated_response = client.futures_get_order(symbol=symbol, orderId=response['orderId'])
                response = updated_response
            except Exception as e:
                logger.warning(f"Could not fetch updated market order details: {e}")

        logger.info(f"MARKET order executed successfully. Response: {response}")
        return response
        
    except BinanceAPIException as e:
        logger.error(f"Binance API Error during MARKET order: [{e.status_code}] {e.message}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during MARKET order: {e}", exc_info=True)
        raise

def place_limit_order(
    symbol: str, 
    side: str, 
    quantity: float, 
    price: float
) -> Dict[str, Any]:
    """
    Places a LIMIT order on Binance Futures Testnet.
    Uses timeInForce="GTC" (Good Till Cancelled).
    """
    logger.info(f"Preparing LIMIT {side} order for {quantity} {symbol} at price {price}")
    client = get_client()
    
    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=price
        )
        logger.info(f"LIMIT order placed successfully. Response: {response}")
        return response
        
    except BinanceAPIException as e:
        logger.error(f"Binance API Error during LIMIT order: [{e.status_code}] {e.message}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during LIMIT order: {e}", exc_info=True)
        raise
