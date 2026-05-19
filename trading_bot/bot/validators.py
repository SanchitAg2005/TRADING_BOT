from typing import Optional
from .logging_config import logger

def validate_symbol(symbol: str) -> str:
    """Validate and format trading symbol."""
    symbol = symbol.upper().strip()
    if not symbol.isalnum():
        logger.warning(f"Validation failed: Invalid symbol format '{symbol}'")
        raise ValueError(f"Invalid symbol '{symbol}'. Must be alphanumeric (e.g., BTCUSDT).")
    return symbol

def validate_side(side: str) -> str:
    """Validate order side (BUY/SELL)."""
    side = side.upper().strip()
    if side not in ("BUY", "SELL"):
        logger.warning(f"Validation failed: Invalid side '{side}'")
        raise ValueError("Side must be either 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type: str) -> str:
    """Validate order type (MARKET/LIMIT)."""
    order_type = order_type.upper().strip()
    if order_type not in ("MARKET", "LIMIT"):
        logger.warning(f"Validation failed: Invalid order type '{order_type}'")
        raise ValueError("Order type must be either 'MARKET' or 'LIMIT'.")
    return order_type

def validate_quantity(quantity: float) -> float:
    """Validate order quantity."""
    if quantity <= 0:
        logger.warning(f"Validation failed: Invalid quantity '{quantity}'")
        raise ValueError("Quantity must be strictly greater than 0.")
    return quantity

def validate_price(order_type: str, price: Optional[float]) -> Optional[float]:
    """Validate price based on order type."""
    if order_type == "LIMIT":
        if price is None or price <= 0:
            logger.warning(f"Validation failed: LIMIT order missing valid price '{price}'")
            raise ValueError("LIMIT orders require a price greater than 0.")
        return price
    
    # For MARKET orders, ignore price if provided
    if price is not None:
        logger.info("Price provided for MARKET order. It will be ignored.")
    return None
