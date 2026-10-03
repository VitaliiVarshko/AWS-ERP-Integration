from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    order_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    customer: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )


from .order_items import OrderItem