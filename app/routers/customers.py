import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.db import get_db
from app.schemas import Customer, CustomerCreate, CustomerUpdate

router = APIRouter(prefix="/customers", tags=["customers"])


def _get_or_404(conn: sqlite3.Connection, customer_id: int) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return row


@router.post("", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(body: CustomerCreate, conn: sqlite3.Connection = Depends(get_db)):
    cur = conn.execute(
        "INSERT INTO customers (name, phone, email, address) VALUES (?, ?, ?, ?)",
        (body.name, body.phone, body.email, body.address),
    )
    conn.commit()
    return dict(_get_or_404(conn, cur.lastrowid))


@router.get("", response_model=list[Customer])
def list_customers(conn: sqlite3.Connection = Depends(get_db)):
    rows = conn.execute("SELECT * FROM customers ORDER BY id").fetchall()
    return [dict(r) for r in rows]


@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id: int, conn: sqlite3.Connection = Depends(get_db)):
    return dict(_get_or_404(conn, customer_id))


@router.patch("/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, body: CustomerUpdate, conn: sqlite3.Connection = Depends(get_db)):
    _get_or_404(conn, customer_id)
    changes = body.model_dump(exclude_unset=True)
    if None in (changes.get("name", ""), changes.get("phone", "")):
        raise HTTPException(status_code=422, detail="name and phone cannot be null")
    if changes:
        cols = ", ".join(f"{k} = ?" for k in changes)
        conn.execute(f"UPDATE customers SET {cols} WHERE id = ?", (*changes.values(), customer_id))
        conn.commit()
    return dict(_get_or_404(conn, customer_id))


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, conn: sqlite3.Connection = Depends(get_db)):
    _get_or_404(conn, customer_id)
    has_jobs = conn.execute("SELECT 1 FROM jobs WHERE customer_id = ? LIMIT 1", (customer_id,)).fetchone()
    if has_jobs:
        raise HTTPException(status_code=409, detail="Customer has jobs; delete or reassign them first")
    conn.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    return Response(status_code=204)
