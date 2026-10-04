import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Order
from ..order_items import OrderItem
from ..schemas import OrderCreate
from ..s3_service import upload_document

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(
        order_number=order.order_number,
        customer=order.customer
    )

    for item in order.items:
        db_order.items.append(
            OrderItem(
                product=item.product,
                quantity=item.quantity
            )
        )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return {
        "id": db_order.id,
        "order_number": db_order.order_number,
        "customer": db_order.customer,
        "items": [
            {
                "product": item.product,
                "quantity": item.quantity
            }
            for item in db_order.items
        ]
    }


@router.get("")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()

    return [
        {
            "id": order.id,
            "order_number": order.order_number,
            "customer": order.customer,
            "items": [
                {
                    "product": item.product,
                    "quantity": item.quantity
                }
                for item in order.items
            ]
        }
        for order in orders
    ]


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "id": order.id,
        "order_number": order.order_number,
        "customer": order.customer,
        "items": [
            {
                "product": item.product,
                "quantity": item.quantity
            }
            for item in order.items
        ]
    }


@router.post("/{order_id}/document")
def save_order_document(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    document = {
        "order_number": order.order_number,
        "customer": order.customer,
        "items": [
            {
                "product": item.product,
                "quantity": item.quantity
            }
            for item in order.items
        ]
    }

    object_key = f"orders/{order.order_number}.json"

    upload_document(
        json.dumps(document, ensure_ascii=False),
        object_key
    )

    return {
        "status": "uploaded",
        "s3_object": object_key
    }

