from pydantic import BaseModel
from typing import Literal


type PizzaSize = Literal["small", "medium", "large"]


class Pizza(BaseModel):
    id: int
    name: str
    size: PizzaSize
    price: float


type OrderStatus = Literal["pending", "ready_to_be_delivered", "cancelled"]


class Order(BaseModel):
    id: int
    pizza_id: int
    quantity: int
    address: str
    status: OrderStatus = "pending"


class User(BaseModel):
    id: int
    name: str
    is_admin: bool = False


class AdminToken(BaseModel):
    token: str
