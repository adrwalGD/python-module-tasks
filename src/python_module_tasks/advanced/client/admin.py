import typer
import requests

from python_module_tasks.advanced.client.const import API_BASE_URL

app = typer.Typer()


@app.command()
def admin_action(token: str = typer.Option()):
    """Perform an dummy admin action (requires a valid admin token)."""
    headers = {"token": token}
    response = requests.get(f"{API_BASE_URL}/admin/admin-action", headers=headers)
    if response.status_code == 200:
        typer.echo(f"Admin action performed successfully.")
    else:
        typer.echo(f"Unauthorized: {response.json()['detail']}")


@app.command()
def create_pizza(
    name: str = typer.Option(),
    size: str = typer.Option(),
    price: float = typer.Option(),
    token: str = typer.Option(),
):
    """Add a new pizza to the menu (admin only)."""
    headers = {"token": token}
    payload = {"name": name, "size": size, "price": price}
    response = requests.post(
        f"{API_BASE_URL}/admin/menu", json=payload, headers=headers
    )
    if response.status_code == 200:
        typer.echo(f"Pizza added to the menu: {response.json()}")
    else:
        typer.echo(f"Failed to add pizza: {response.json()['detail']}")


@app.command()
def delete_pizza(
    pizza_id: int = typer.Option(),
    token: str = typer.Option(),
):
    """Delete a pizza from the menu (admin only)."""
    headers = {"token": token}
    response = requests.delete(f"{API_BASE_URL}/admin/menu/{pizza_id}", headers=headers)
    if response.status_code == 200:
        typer.echo(f"Pizza deleted from the menu.")
    else:
        typer.echo(f"Failed to delete pizza: {response.json()['detail']}")


@app.command()
def cancel_order(
    order_id: int = typer.Option(),
    token: str = typer.Option(),
):
    """Force cancel an order (admin only)."""
    headers = {"token": token}
    response = requests.delete(
        f"{API_BASE_URL}/admin/order/{order_id}", headers=headers
    )
    if response.status_code == 200:
        typer.echo(f"Order cancelled.")
    else:
        typer.echo(f"Failed to cancel order: {response.json()['detail']}")
