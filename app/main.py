import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .database import Base, engine
from .models import Order
from .order_items import OrderItem
from .routers.orders import router as orders_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

app = FastAPI(title="ERP Integration API")

Base.metadata.create_all(bind=engine)

app.include_router(orders_router)

@app.get("/ui", response_class=HTMLResponse)
def ui():
    html_file = Path(__file__).parent / "templates" / "index.html"
    return html_file.read_text(encoding="utf-8")

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
