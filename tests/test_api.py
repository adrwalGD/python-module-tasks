from fastapi.testclient import TestClient
from python_module_tasks.advanced.api.main import app

client = TestClient(app)


def test_list_menu():
    response = client.get("/customer/menu")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "id" in response.json()[0]


def test_create_order():
    payload = {"pizza_id": 1, "quantity": 2}
    response = client.post("/customer/order", json=payload)
    assert response.status_code == 200
    assert response.json()["id"]
    assert response.json()["pizza_id"] == payload["pizza_id"]


def test_check_order_status():
    create_response = client.post(
        "/customer/order", json={"pizza_id": 1, "quantity": 2}
    )
    order_id = create_response.json()["id"]

    response = client.get(f"/customer/order/{order_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "pending"


def test_cancel_order():
    create_response = client.post(
        "/customer/order", json={"pizza_id": 1, "quantity": 2}
    )
    order_id = create_response.json()["id"]

    response = client.delete(f"/customer/order/{order_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Order cancelled"


def test_admin_action_unauthorized():
    headers = {"token": "invalid_token"}
    response = client.get("/admin/admin-action", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
