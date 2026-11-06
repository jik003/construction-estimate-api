import sqlite3
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.db import get_db
from app.schemas import Job, JobCreate, JobStatus, JobUpdate

router = APIRouter(prefix="/jobs", tags=["jobs"])

NOT_NULL_FIELDS = {"title", "job_type", "site_address"}


def _get_or_404(conn: sqlite3.Connection, job_id: int) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return row


def _to_db(values: dict) -> dict:
    """Enums -> str, dates -> 'YYYY-MM-DD'."""
    out = {}
    for k, v in values.items():
        if hasattr(v, "value"):
            v = v.value
        elif hasattr(v, "isoformat"):
            v = v.isoformat()
        out[k] = v
    return out


@router.post("", response_model=Job, status_code=status.HTTP_201_CREATED)
def create_job(body: JobCreate, conn: sqlite3.Connection = Depends(get_db)):
    exists = conn.execute("SELECT 1 FROM customers WHERE id = ?", (body.customer_id,)).fetchone()
    if not exists:
        raise HTTPException(status_code=404, detail="Customer not found")
    data = _to_db(body.model_dump())
    cols = ", ".join(data)
    marks = ", ".join("?" for _ in data)
    cur = conn.execute(f"INSERT INTO jobs ({cols}) VALUES ({marks})", tuple(data.values()))
    conn.commit()
    return dict(_get_or_404(conn, cur.lastrowid))


@router.get("", response_model=list[Job])
def list_jobs(
    status: Optional[JobStatus] = None,
    customer_id: Optional[int] = None,
    conn: sqlite3.Connection = Depends(get_db),
):
    sql, params = "SELECT * FROM jobs WHERE 1=1", []
    if status is not None:
        sql += " AND status = ?"
        params.append(status.value)
    if customer_id is not None:
        sql += " AND customer_id = ?"
        params.append(customer_id)
    rows = conn.execute(sql + " ORDER BY id", params).fetchall()
    return [dict(r) for r in rows]


@router.get("/{job_id}", response_model=Job)
def get_job(job_id: int, conn: sqlite3.Connection = Depends(get_db)):
    return dict(_get_or_404(conn, job_id))


@router.patch("/{job_id}", response_model=Job)
def update_job(job_id: int, body: JobUpdate, conn: sqlite3.Connection = Depends(get_db)):
    current = _get_or_404(conn, job_id)
    changes = _to_db(body.model_dump(exclude_unset=True))
    if any(changes.get(f, "") is None for f in NOT_NULL_FIELDS):
        raise HTTPException(status_code=422, detail=f"{sorted(NOT_NULL_FIELDS)} cannot be null")

    # date range must stay valid against the values already stored
    start = changes.get("scheduled_start", current["scheduled_start"])
    end = changes.get("scheduled_end", current["scheduled_end"])
    if start and end and end < start:
        raise HTTPException(status_code=422, detail="scheduled_end must be on or after scheduled_start")

    if changes:
        cols = ", ".join(f"{k} = ?" for k in changes)
        conn.execute(
            f"UPDATE jobs SET {cols}, updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now') WHERE id = ?",
            (*changes.values(), job_id),
        )
        conn.commit()
    return dict(_get_or_404(conn, job_id))


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, conn: sqlite3.Connection = Depends(get_db)):
    _get_or_404(conn, job_id)
    conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    return Response(status_code=204)
