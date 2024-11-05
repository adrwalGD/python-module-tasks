import os
from dotenv import load_dotenv

load_dotenv()

from fastapi.testclient import TestClient
from python_module_tasks.advanced.api.main import app
from python_module_tasks.advanced.api.models import Order, Pizza
from pydantic import ValidationError
from python_module_tasks.advanced.api.routes.customer import orders
import pytest

client = TestClient(app)


class TestCustomerRoutes:
    def test_list_menu(self):
        response = client.get("/customer/menu")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        for item in response.json():
            try:
                Pizza(**item)
            except ValidationError as e:
                pytest.fail(f"ValidationError on Pizza model: {e}")
            except Exception as e:
                pytest.fail(f"Unexpected error: {e}")

    def test_create_order(self):
        payload = {"pizza_id": 1, "quantity": 2, "address": "123 Main St"}
        response = client.post("/customer/order", json=payload)
        assert response.status_code == 200
        try:
            Order(**response.json())
        except ValidationError as e:
            pytest.fail(f"ValidationError on Order model: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")

    def test_check_order_status(self):
        create_response = client.post(
            "/customer/order",
            json={"pizza_id": 1, "quantity": 2, "address": "123 Main St"},
        )
        order_id = create_response.json()["id"]

        response = client.get(f"/customer/order/{order_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "pending"
        try:
            Order(**response.json())
        except ValidationError as e:
            pytest.fail(f"ValidationError on Order model: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")

    def test_cancel_order(self):
        create_response = client.post(
            "/customer/order",
            json={"pizza_id": 1, "quantity": 2, "address": "123 Main St"},
        )
        order_id = create_response.json()["id"]

        response = client.delete(f"/customer/order/{order_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Order cancelled"
        assert orders[order_id].status == "cancelled"


class TestAdminRoutes:
    admin_token = os.getenv("ADMIN_TOKEN", "")

    def test_admin_action_unauthorized(self):
        headers = {"token": "invalid_token"}
        response = client.get("/admin/admin-action", headers=headers)
        assert response.status_code == 401
        assert response.json()["detail"] == "Unauthorized"

    def test_admin_action_authorized(self):
        headers = {"token": self.admin_token}
        response = client.get("/admin/admin-action", headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Admin action successful"

    def test_create_pizza(self):
        headers = {"token": self.admin_token}
        payload = {"id": 3, "name": "Hawaiian", "size": "large", "price": 13.99}
        response = client.post("/admin/menu", json=payload, headers=headers)
        assert response.status_code == 200
        assert response.json() == payload

    def test_delete_pizza(self):
        headers = {"token": self.admin_token}
        pizza_id = 1
        response = client.delete(f"/admin/menu/{pizza_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Pizza deleted"

    def test_cancel_order(self):
        headers = {"token": self.admin_token}
        create_response = client.post(
            "/customer/order",
            json={"pizza_id": 1, "quantity": 2, "address": "123 Main St"},
        )
        order_id = create_response.json()["id"]

        response = client.delete(f"/admin/order/{order_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Order cancelled"
        assert orders[order_id].status == "cancelled"

    def test_cancel_order_order_not_found(self):
        headers = {"token": self.admin_token}
        response = client.delete("/admin/order/999", headers=headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Order not found"
