from fastapi import FastAPI

from .database import Base, engine
from .models import Order
from .order_items import OrderItem
from .routers.orders import router as orders_router


app = FastAPI(title="ERP Integration API")

Base.metadata.create_all(bind=engine)

app.include_router(orders_router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "ERP Integration API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }