from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class OrderStatus(str, enum.Enum):
    PENDING = "Pending"
    ASSIGNED = "Assigned"
    LOADING = "Loading"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

class VehicleStatus(str, enum.Enum):
    AVAILABLE = "Available"
    ASSIGNED = "Assigned"
    LOADING = "Loading"
    ON_TRIP = "On Trip"
    MAINTENANCE = "Maintenance"
    INACTIVE = "Inactive"

class DriverStatus(str, enum.Enum):
    AVAILABLE = "Available"
    ASSIGNED = "Assigned"
    ON_TRIP = "On Trip"
    LEAVE = "Leave"
    INACTIVE = "Inactive"

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    contact_number = Column(String)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    gst_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicles = relationship("Vehicle", back_populates="company")
    drivers = relationship("Driver", back_populates="company")
    orders = relationship("Order", back_populates="company")
    trips = relationship("TripHistory", back_populates="company")
    notifications = relationship("Notification", back_populates="company")

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    vehicle_number = Column(String, index=True)
    type = Column(String) # Lorry, Container Truck, Trailer, Pickup, Mini Truck, Tanker
    capacity = Column(Float, nullable=True)
    fuel_capacity = Column(Float, nullable=True)
    current_fuel = Column(Float, nullable=True)
    
    # Driver assigned to this vehicle (can be dynamic, but good for 1:1 binding)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    
    status = Column(String, default=VehicleStatus.AVAILABLE)
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)

    company = relationship("Company", back_populates="vehicles")
    driver = relationship("Driver", back_populates="vehicle", foreign_keys=[driver_id])
    orders = relationship("Order", back_populates="vehicle")
    trips = relationship("TripHistory", back_populates="vehicle")
    fuel_records = relationship("FuelRecord", back_populates="vehicle")

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    name = Column(String)
    phone_number = Column(String)
    license_number = Column(String)
    experience_years = Column(Integer)
    status = Column(String, default=DriverStatus.AVAILABLE)

    company = relationship("Company", back_populates="drivers")
    vehicle = relationship("Vehicle", back_populates="driver", foreign_keys=[Vehicle.driver_id])
    orders = relationship("Order", back_populates="driver")
    trips = relationship("TripHistory", back_populates="driver")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    customer_name = Column(String)
    pickup_location = Column(String)
    delivery_location = Column(String)
    material = Column(String)
    weight = Column(Float)
    priority = Column(String)
    
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    
    status = Column(String, default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="orders")
    vehicle = relationship("Vehicle", back_populates="orders")
    driver = relationship("Driver", back_populates="orders")
    trip = relationship("TripHistory", back_populates="order", uselist=False)

class TripHistory(Base):
    __tablename__ = "trip_history"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    
    distance = Column(Float, default=0.0)
    fuel_used = Column(Float, default=0.0)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="trips")
    order = relationship("Order", back_populates="trip")
    vehicle = relationship("Vehicle", back_populates="trips")
    driver = relationship("Driver", back_populates="trips")

class FuelRecord(Base):
    __tablename__ = "fuel_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    date = Column(DateTime, default=datetime.utcnow)
    fuel_filled = Column(Float)
    fuel_cost = Column(Float)
    fuel_station = Column(String)

    vehicle = relationship("Vehicle", back_populates="fuel_records")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    message = Column(String)
    type = Column(String) # e.g. success, info, warning
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="notifications")
