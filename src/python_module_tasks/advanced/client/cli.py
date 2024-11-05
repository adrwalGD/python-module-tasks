import typer

import python_module_tasks.advanced.client.customer as customer
import python_module_tasks.advanced.client.admin as admin

app = typer.Typer()
app.add_typer(customer.app, name="customer")
app.add_typer(admin.app, name="admin")

if __name__ == "__main__":
    app()
