from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import OrderStatus, VehicleStatus, DriverStatus

# ----------------- Auth & Company -----------------
class CompanyCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    contact_number: str

class CompanyLogin(BaseModel):
    email: EmailStr
    password: str

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    contact_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    logo_url: Optional[str] = None
    gst_number: Optional[str] = None

class CompanyOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    contact_number: str
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]
    logo_url: Optional[str]
    gst_number: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True

# ----------------- Vehicle -----------------
class VehicleBase(BaseModel):
    vehicle_number: str
    type: str
    capacity: Optional[float] = None
    fuel_capacity: Optional[float] = None
    current_fuel: Optional[float] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    status: Optional[VehicleStatus] = None
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    current_fuel: Optional[float] = None
    driver_id: Optional[int] = None

class VehicleOut(VehicleBase):
    id: int
    company_id: int
    driver_id: Optional[int]
    status: VehicleStatus
    current_lat: Optional[float]
    current_lng: Optional[float]
    class Config:
        orm_mode = True

# ----------------- Driver -----------------
class DriverBase(BaseModel):
    name: str
    phone_number: str
    license_number: str
    experience_years: int

class DriverCreate(DriverBase):
    pass

class DriverUpdate(BaseModel):
    status: Optional[DriverStatus] = None

class DriverOut(DriverBase):
    id: int
    company_id: int
    status: DriverStatus
    class Config:
        orm_mode = True

# ----------------- Order -----------------
class OrderBase(BaseModel):
    customer_name: str
    pickup_location: str
    delivery_location: str
    material: str
    weight: float
    priority: str
    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderOut(OrderBase):
    id: int
    company_id: int
    status: OrderStatus
    created_at: datetime
    class Config:
        orm_mode = True

# ----------------- Trip History -----------------
class TripHistoryBase(BaseModel):
    order_id: int
    vehicle_id: Optional[int]
    driver_id: Optional[int]
    distance: float = 0.0
    fuel_used: float = 0.0

class TripHistoryCreate(TripHistoryBase):
    pass

class TripHistoryOut(TripHistoryBase):
    id: int
    company_id: int
    start_time: Optional[datetime]
    end_time: datetime
    class Config:
        orm_mode = True

# ----------------- Notifications -----------------
class NotificationOut(BaseModel):
    id: int
    company_id: int
    message: str
    type: str
    created_at: datetime
    class Config:
        orm_mode = True
