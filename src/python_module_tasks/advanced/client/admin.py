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
