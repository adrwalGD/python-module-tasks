from typer.testing import CliRunner
from python_module_tasks.advanced.client.cli import app
import pytest

runner = CliRunner()


@pytest.mark.usefixtures("run_api_server")
def test_list_menu():
    result = runner.invoke(app, ["list-menu"])
    assert result.exit_code == 0
    assert (
        "1: Margherita (large) - $8.99\n2: Pepperoni (large) - $12.99\n"
        in result.output
    )


@pytest.mark.usefixtures("run_api_server")
def test_create_order():
    result = runner.invoke(app, ["create-order", "--pizza-id", "1", "--quantity", "2"])
    assert result.exit_code == 0
    assert "Order created with ID:" in result.output


@pytest.mark.usefixtures("run_api_server")
def test_check_order_status():
    order_result = runner.invoke(
        app, ["create-order", "--pizza-id", "1", "--quantity", "2"]
    )
    order_id = int(order_result.output.split("ID:")[1].strip())

    result = runner.invoke(app, ["check-order-status", "--order-id", str(order_id)])
    assert result.exit_code == 0
    assert "Status: pending" in result.output


@pytest.mark.usefixtures("run_api_server")
def test_cancel_order():
    order_result = runner.invoke(
        app, ["create-order", "--pizza-id", "1", "--quantity", "2"]
    )
    order_id = int(order_result.output.split("ID:")[1].strip())

    result = runner.invoke(app, ["cancel-order", "--order-id", str(order_id)])
    assert result.exit_code == 0
    assert "Order cancelled successfully" in result.output


@pytest.mark.usefixtures("run_api_server")
def test_admin_action_unauthorized():
    result = runner.invoke(app, ["admin-action", "--token", "invalid_token"])
    assert result.exit_code == 0
    assert "Unauthorized" in result.output


@pytest.mark.usefixtures("run_api_server")
def test_admin_action_authorized():
    result = runner.invoke(app, ["admin-action", "--token", "hardcoded_admin_token"])
    assert result.exit_code == 0
    assert "Admin action performed successfully." in result.output
