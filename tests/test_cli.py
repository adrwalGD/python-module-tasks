from dotenv import load_dotenv

load_dotenv()

from typer.testing import CliRunner
from python_module_tasks.advanced.client.cli import app
import pytest

runner = CliRunner()


class TestCustomer:
    @pytest.mark.usefixtures("run_api_server")
    def test_list_menu(self):
        result = runner.invoke(app, ["customer", "list-menu"])
        assert result.exit_code == 0
        assert (
            "1: Margherita (large) - $8.99\n2: Pepperoni (large) - $12.99\n"
            in result.output
        )

    @pytest.mark.usefixtures("run_api_server")
    def test_create_order(self):
        result = runner.invoke(
            app,
            [
                "customer",
                "create-order",
                "--pizza-id",
                "1",
                "--quantity",
                "2",
                "--address",
                "123 Main St",
            ],
        )
        assert result.exit_code == 0
        assert "Order created with ID:" in result.output

    @pytest.mark.usefixtures("run_api_server")
    def test_check_order_status(self):
        order_result = runner.invoke(
            app,
            [
                "customer",
                "create-order",
                "--pizza-id",
                "1",
                "--quantity",
                "2",
                "--address",
                "123 Main St",
            ],
        )
        order_id = int(order_result.output.split("ID:")[1].strip())

        result = runner.invoke(
            app, ["customer", "check-order-status", "--order-id", str(order_id)]
        )
        assert result.exit_code == 0
        assert "Status: pending" in result.output

    @pytest.mark.usefixtures("run_api_server")
    def test_cancel_order(self):
        order_result = runner.invoke(
            app,
            [
                "customer",
                "create-order",
                "--pizza-id",
                "1",
                "--quantity",
                "2",
                "--address",
                "123 Main St",
            ],
        )
        order_id = int(order_result.output.split("ID:")[1].strip())

        result = runner.invoke(
            app, ["customer", "cancel-order", "--order-id", str(order_id)]
        )
        assert result.exit_code == 0
        assert "Order cancelled successfully" in result.output


class TestAdmin:
    @pytest.mark.usefixtures("run_api_server")
    def test_admin_action_unauthorized(self):
        result = runner.invoke(
            app, ["admin", "admin-action", "--token", "invalid_token"]
        )
        assert result.exit_code == 0
        assert "Unauthorized" in result.output

    @pytest.mark.usefixtures("run_api_server")
    def test_admin_action_authorized(self):
        result = runner.invoke(
            app, ["admin", "admin-action", "--token", "hardcoded_admin_token"]
        )
        assert result.exit_code == 0
        assert "Admin action performed successfully." in result.output

    @pytest.mark.usefixtures("run_api_server")
    def test_create_pizza(self):
        result = runner.invoke(
            app,
            [
                "admin",
                "create-pizza",
                "--name",
                "Hawaiian",
                "--size",
                "large",
                "--price",
                "14.99",
                "--token",
                "hardcoded_admin_token",
            ],
        )
        assert result.exit_code == 0
        assert "Pizza added to the menu" in result.output

    @pytest.mark.usefixtures("run_api_server")
    def test_delete_pizza(self):
        result = runner.invoke(
            app,
            [
                "admin",
                "delete-pizza",
                "--pizza-id",
                "1",
                "--token",
                "hardcoded_admin_token",
            ],
        )
        assert result.exit_code == 0
        assert "Pizza deleted from the menu" in result.output

    @pytest.mark.usefixtures("run_api_server")
    def test_cancel_order(self):
        order_result = runner.invoke(
            app,
            [
                "customer",
                "create-order",
                "--pizza-id",
                "1",
                "--quantity",
                "2",
                "--address",
                "123 Main St",
            ],
        )
        order_id = int(order_result.output.split("ID:")[1].strip())

        result = runner.invoke(
            app,
            [
                "admin",
                "cancel-order",
                "--order-id",
                str(order_id),
                "--token",
                "hardcoded_admin_token",
            ],
        )
        assert result.exit_code == 0
        assert "Order cancelled" in result.output
