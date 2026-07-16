from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from config import DATABASE_URL
from database.api import get_database, get_tables_handle
from database.schemas.probe import (
    Address,
    Base,
    Category,
    Customer,
    Employee,
    Order,
    OrderItem,
    Payment,
    Product,
    Role,
    Supplier,
)


def seed(session: Session) -> None:
    # Roles + employees
    admin = Role(name="admin", description="Full access")
    support = Role(name="support", description="Handles customer tickets")
    session.add_all(
        [
            Employee(role=admin, email="alice@shop.test", full_name="Alice Admin"),
            Employee(role=support, email="bob@shop.test", full_name="Bob Support"),
        ]
    )

    # Customers + addresses
    carol = Customer(email="carol@mail.test", full_name="Carol Buyer", phone="+351911111111")
    dave = Customer(email="dave@mail.test", full_name="Dave Buyer")
    carol.addresses.append(
        Address(line1="Rua A 1", city="Lisbon", postal_code="1000-001", country="PT")
    )
    dave.addresses.append(
        Address(label="work", line1="Main St 42", city="Porto", postal_code="4000-002", country="PT")
    )
    session.add_all([carol, dave])

    # Catalog: suppliers, categories, products
    acme = Supplier(name="Acme Goods", contact_email="sales@acme.test")
    electronics = Category(name="Electronics")
    phones = Category(name="Phones", parent=electronics)
    books = Category(name="Books")

    phone = Product(sku="PH-001", name="SmartPhone X", price=Decimal("599.99"), stock=25, category=phones, supplier=acme)
    charger = Product(sku="AC-010", name="USB-C Charger", price=Decimal("19.90"), stock=200, category=electronics, supplier=acme)
    novel = Product(sku="BK-100", name="A Good Novel", price=Decimal("12.50"), stock=80, category=books)
    session.add_all([acme, electronics, phones, books, phone, charger, novel])

    # An order for Carol with two line items and a payment
    order = Order(customer=carol, status="paid")
    order.items.append(OrderItem(product=phone, quantity=1, unit_price=phone.price))
    order.items.append(OrderItem(product=charger, quantity=2, unit_price=charger.price))
    total = sum((i.unit_price * i.quantity for i in order.items), Decimal("0"))
    order.payment = Payment(
        amount=total,
        method="card",
        status="captured",
        paid_at=datetime.now(timezone.utc),
    )
    session.add(order)


def main() -> None:
    db = get_database(DATABASE_URL)
    tables = get_tables_handle(db)
    tables.drop_all(Base.metadata)
    tables.create_all(Base.metadata)
    with db.session() as session:
        seed(session)
        session.commit()
    print("Seed complete.")


if __name__ == "__main__":
    main()
