from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product: str
    quantity: int


class OrderCreate(BaseModel):
    order_number: str
    customer: str
    items: list[OrderItemCreate]