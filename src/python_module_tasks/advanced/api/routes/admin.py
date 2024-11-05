import os
from fastapi import APIRouter, HTTPException, Depends, Header

from python_module_tasks.advanced.api.models import Pizza, PizzaSize
from python_module_tasks.advanced.api.routes.customer import pizzas, orders
from pydantic import BaseModel

router = APIRouter()


def admin_auth(token: str = Header()):
    if token != os.getenv("ADMIN_TOKEN"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


@router.get("/admin-action", dependencies=[Depends(admin_auth)])
async def perform_admin_action():
    """Perform an admin action (dummy)"""
    return {"message": "Admin action successful"}


class CreatePizzaBody(BaseModel):
    name: str
    size: PizzaSize
    price: float


@router.post("/menu", dependencies=[Depends(admin_auth)])
async def create_pizza(body: CreatePizzaBody):
    """Add new pizza to the menu (admin only)"""
    global pizzas
    pizza = Pizza(id=len(pizzas) + 1, name=body.name, size=body.size, price=body.price)
    pizzas.append(pizza)
    return pizza


@router.delete("/menu/{pizza_id}", dependencies=[Depends(admin_auth)])
async def delete_pizza(pizza_id: int):
    """Delete a pizza from the menu (admin only)"""
    global pizzas
    if pizza_id not in [pizza.id for pizza in pizzas]:
        raise HTTPException(status_code=404, detail="Pizza not found")

    pizzas = [pizza for pizza in pizzas if pizza.id != pizza_id]
    return {"message": "Pizza deleted"}


@router.delete("/order/{order_id}", dependencies=[Depends(admin_auth)])
async def cancel_order(order_id: int):
    """Force cancel an order (admin only)"""
    global orders
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "cancelled"
    return {"message": "Order cancelled"}
