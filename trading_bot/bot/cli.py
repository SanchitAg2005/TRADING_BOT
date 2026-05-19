import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
from binance.exceptions import BinanceAPIException
from requests.exceptions import RequestException

from . import validators
from . import orders
from .logging_config import logger

app = typer.Typer(help="Binance Futures Testnet Trading CLI Bot")
console = Console()

def display_success(response: dict, order_type: str):
    """Renders a beautiful success table using Rich."""
    table = Table(title="[bold green]Order Executed Successfully[/bold green]")
    
    table.add_column("Field", style="cyan", justify="right")
    table.add_column("Value", style="magenta")

    table.add_row("Order ID", str(response.get("orderId", "N/A")))
    table.add_row("Symbol", response.get("symbol", "N/A"))
    table.add_row("Side", response.get("side", "N/A"))
    table.add_row("Type", response.get("type", order_type))
    table.add_row("Final Status", response.get("status", "N/A"))
    
    # Handle different keys for executed quantity
    executed_qty = response.get("executedQty") or response.get("cumQty", "0")
    table.add_row("Executed Qty", str(executed_qty))
    
    avg_price = response.get("avgPrice")
    if avg_price and float(avg_price) > 0:
        table.add_row("Average Price", str(avg_price))
    elif response.get("price") and float(response.get("price", 0)) > 0:
        table.add_row("Limit Price", str(response.get("price")))

    # Parse and add transactTime/updateTime if available
    transact_time = response.get("updateTime") or response.get("time") or response.get("transactTime")
    if transact_time:
        import datetime
        try:
            # Binance returns time in milliseconds
            dt_obj = datetime.datetime.fromtimestamp(int(transact_time) / 1000.0)
            table.add_row("Transact Time", dt_obj.strftime("%Y-%m-%d %H:%M:%S"))
        except (ValueError, TypeError):
            table.add_row("Transact Time", str(transact_time))

    console.print(table)

def display_error(title: str, message: str):
    """Renders a beautiful error panel using Rich."""
    panel = Panel(
        f"[bold red]{message}[/bold red]", 
        title=f"[bold red]Error: {title}[/bold red]",
        border_style="red"
    )
    console.print(panel)

@app.command()
def trade(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair symbol (e.g., BTCUSDT)"),
    side: str = typer.Option(..., "--side", "-d", help="Order side: BUY or SELL"),
    order_type: str = typer.Option(..., "--type", "-t", help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="Quantity to trade"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Price (Required for LIMIT orders)")
):
    """
    Execute a trade on Binance Futures Testnet.
    """
    logger.info(f"CLI Trade command invoked: {symbol} {side} {order_type} qty={quantity} price={price}")
    
    try:
        # 1. Validation
        clean_symbol = validators.validate_symbol(symbol)
        clean_side = validators.validate_side(side)
        clean_type = validators.validate_order_type(order_type)
        clean_qty = validators.validate_quantity(quantity)
        clean_price = validators.validate_price(clean_type, price)

        # 2. Execution
        with console.status(f"[bold yellow]Placing {clean_type} order for {clean_qty} {clean_symbol}...[/bold yellow]"):
            if clean_type == "MARKET":
                response = orders.place_market_order(clean_symbol, clean_side, clean_qty)
            else:
                response = orders.place_limit_order(clean_symbol, clean_side, clean_qty, clean_price)

        # 3. Output
        display_success(response, clean_type)

    except ValueError as ve:
        # Handle user input validation errors gracefully
        display_error("Validation Failed", str(ve))
        raise typer.Exit(code=1)
        
    except BinanceAPIException as bae:
        # Handle Binance API errors (e.g. minQty, invalid symbol on exchange side)
        display_error("Binance API Exception", f"Code {bae.status_code}: {bae.message}")
        raise typer.Exit(code=1)
        
    except RequestException as re:
        # Handle Network errors gracefully
        logger.error(f"Network error: {re}", exc_info=True)
        display_error("Network Error", "Could not connect to Binance API. Check your internet connection or try again later.")
        raise typer.Exit(code=1)
        
    except Exception as e:
        # Catch all other unexpected errors
        display_error("Unexpected Error", f"An unexpected error occurred: {str(e)}\nCheck logs for details.")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
