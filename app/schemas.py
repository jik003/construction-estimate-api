from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class JobType(str, Enum):
    construction = "construction"
    design = "design"
    electrical = "electrical"
    roofing = "roofing"
    repair = "repair"
    interior = "interior"
    woodworking = "woodworking"


class JobStatus(str, Enum):
    inquiry = "inquiry"
    estimating = "estimating"
    contracted = "contracted"
    in_progress = "in_progress"
    completed = "completed"
    settled = "settled"
    cancelled = "cancelled"


def _check_phone(v: Optional[str]) -> Optional[str]:
    if v is None:
        return v
    v = v.strip()
    if not all(c.isdigit() or c == "-" for c in v):
        raise ValueError("phone may contain only digits and '-'")
    digits = sum(c.isdigit() for c in v)
    if not 9 <= digits <= 15:
        raise ValueError("phone must have 9-15 digits")
    return v


# ---------- Customers ----------

class CustomerBase(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50)
    phone: str
    email: Optional[str] = Field(default=None, max_length=254)
    address: Optional[str] = Field(default=None, max_length=200)

    check_phone = field_validator("phone")(_check_phone)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    phone: Optional[str] = None
    email: Optional[str] = Field(default=None, max_length=254)
    address: Optional[str] = Field(default=None, max_length=200)

    check_phone = field_validator("phone")(_check_phone)


class Customer(CustomerBase):
    model_config = ConfigDict(extra="ignore")

    id: int
    created_at: str


# ---------- Jobs ----------

class _DateRangeMixin:
    @model_validator(mode="after")
    def _check_dates(self):
        start, end = self.scheduled_start, self.scheduled_end
        if start and end and end < start:
            raise ValueError("scheduled_end must be on or after scheduled_start")
        return self


class JobCreate(_DateRangeMixin, BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    customer_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=100)
    job_type: JobType
    site_address: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    scheduled_start: Optional[date] = None
    scheduled_end: Optional[date] = None


class JobUpdate(_DateRangeMixin, BaseModel):
    # status is intentionally NOT here: it changes only via POST /jobs/{id}/status (week 3)
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    job_type: Optional[JobType] = None
    site_address: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    scheduled_start: Optional[date] = None
    scheduled_end: Optional[date] = None


class Job(BaseModel):
    id: int
    customer_id: int
    title: str
    job_type: JobType
    site_address: str
    description: Optional[str]
    status: JobStatus
    scheduled_start: Optional[str]
    scheduled_end: Optional[str]
    created_at: str
    updated_at: str
