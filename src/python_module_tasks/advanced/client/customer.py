import typer
import requests

from python_module_tasks.advanced.client.const import API_BASE_URL

app = typer.Typer()


@app.command()
def list_menu():
    """List available pizzas on the menu."""
    response = requests.get(f"{API_BASE_URL}/customer/menu")
    if response.status_code == 200:
        menu = response.json()
        for pizza in menu:
            typer.echo(
                f"{pizza['id']}: {pizza['name']} ({pizza['size']}) - ${pizza['price']}"
            )
    else:
        typer.echo("Failed to retrieve the menu.")


@app.command()
def create_order(
    pizza_id: int = typer.Option(),
    quantity: int = typer.Option(),
    address: str = typer.Option(),
):
    """Create a new order for a pizza."""
    payload = {"pizza_id": pizza_id, "quantity": quantity, "address": address}
    response = requests.post(f"{API_BASE_URL}/customer/order", json=payload)
    if response.status_code == 200:
        order = response.json()
        typer.echo(f"Order created with ID: {order['id']}")
    else:
        typer.echo(f"Failed to create order: {response.json()['detail']}")


@app.command()
def check_order_status(order_id: int = typer.Option()):
    """Check the status of an order."""
    response = requests.get(f"{API_BASE_URL}/customer/order/{order_id}")
    if response.status_code == 200:
        order = response.json()
        typer.echo(f"Order ID: {order['id']}, Status: {order['status']}")
    else:
        typer.echo(f"Failed to retrieve order status: {response.json()['detail']}")


@app.command()
def cancel_order(order_id: int = typer.Option()):
    """Cancel an order if it's not ready to be delivered."""
    response = requests.delete(f"{API_BASE_URL}/customer/order/{order_id}")
    if response.status_code == 200:
        typer.echo("Order cancelled successfully.")
    else:
        typer.echo(f"Failed to cancel order: {response.json()['detail']}")


if __name__ == "__main__":
    app()
