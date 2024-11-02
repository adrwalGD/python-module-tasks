from typer.testing import CliRunner
from python_module_tasks.advanced.client.cli import app

runner = CliRunner()


def test_list_menu():
    result = runner.invoke(app, ["list-menu"])
    assert result.exit_code == 0
    assert "Margherita" in result.output


def test_create_order():
    result = runner.invoke(app, ["create-order", "--pizza-id", "1", "--quantity", "2"])
    assert result.exit_code == 0
    assert "Order created with ID:" in result.output


def test_check_order_status():
    order_result = runner.invoke(
        app, ["create-order", "--pizza-id", "1", "--quantity", "2"]
    )
    order_id = int(order_result.output.split("ID:")[1].strip())

    result = runner.invoke(app, ["check-order-status", "--order-id", str(order_id)])
    assert result.exit_code == 0
    assert "Status:" in result.output


def test_cancel_order():
    order_result = runner.invoke(
        app, ["create-order", "--pizza-id", "1", "--quantity", "2"]
    )
    order_id = int(order_result.output.split("ID:")[1].strip())

    result = runner.invoke(app, ["cancel-order", "--order-id", str(order_id)])
    assert result.exit_code == 0
    assert "Order cancelled successfully" in result.output


def test_admin_action_unauthorized():
    result = runner.invoke(app, ["admin-action", "--token", "invalid_token"])
    assert result.exit_code == 0
    assert "Unauthorized" in result.output
