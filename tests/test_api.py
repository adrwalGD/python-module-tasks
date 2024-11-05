from fastapi.testclient import TestClient
from python_module_tasks.advanced.api.main import app
from python_module_tasks.advanced.api.models import Order, Pizza
from pydantic import ValidationError
from python_module_tasks.advanced.api.routes.customer import orders
import pytest

client = TestClient(app)


def test_list_menu():
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


def test_create_order():
    payload = {"pizza_id": 1, "quantity": 2}
    response = client.post("/customer/order", json=payload)
    assert response.status_code == 200
    try:
        Order(**response.json())
    except ValidationError as e:
        pytest.fail(f"ValidationError on Order model: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


def test_check_order_status():
    create_response = client.post(
        "/customer/order", json={"pizza_id": 1, "quantity": 2}
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


def test_cancel_order():
    create_response = client.post(
        "/customer/order", json={"pizza_id": 1, "quantity": 2}
    )
    order_id = create_response.json()["id"]

    response = client.delete(f"/customer/order/{order_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Order cancelled"
    assert orders[order_id].status == "cancelled"


def test_admin_action_unauthorized():
    headers = {"token": "invalid_token"}
    response = client.get("/admin/admin-action", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
