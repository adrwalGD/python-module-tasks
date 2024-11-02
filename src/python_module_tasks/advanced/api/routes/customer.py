from fastapi import APIRouter, HTTPException
from python_module_tasks.advanced.api.models import Order, Pizza

router = APIRouter()

pizzas = [
    Pizza(id=1, name="Margherita", size="large", price=8.99),
    Pizza(id=2, name="Pepperoni", size="large", price=12.99),
]

orders: dict[int, Order] = {}


@router.get("/menu", response_model=list[Pizza])
async def get_menu():
    return pizzas


@router.post("/order", response_model=Order)
async def create_order(pizza_id: int, quantity: int):
    if pizza_id not in [pizza.id for pizza in pizzas]:
        raise HTTPException(status_code=404, detail="Pizza not found")
    new_order = Order(id=len(orders) + 1, pizza_id=pizza_id, quantity=quantity)
    orders[new_order.id] = new_order
    return new_order


@router.get("/order/{order_id}", response_model=Order)
async def check_order_status(order_id: int):
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/order/{order_id}")
async def cancel_order(order_id: int):
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status == "ready_to_be_delivered":
        raise HTTPException(
            status_code=400, detail="Cannot cancel order that is ready to be delivered"
        )
    order.status = "cancelled"
    return {"message": "Order cancelled"}
