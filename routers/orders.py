from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas, dependencies, database

router = APIRouter(prefix="/api/orders", tags=["orders"])

def create_notification(db: Session, company_id: int, message: str, type: str):
    notif = models.Notification(company_id=company_id, message=message, type=type)
    db.add(notif)
    db.commit()

@router.post("/", response_model=schemas.OrderOut)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    # Determine initial status
    status = models.OrderStatus.PENDING
    if order.vehicle_id and order.driver_id:
        status = models.OrderStatus.ASSIGNED
        
        # Validate they are available
        vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == order.vehicle_id, models.Vehicle.company_id == current_company.id).first()
        driver = db.query(models.Driver).filter(models.Driver.id == order.driver_id, models.Driver.company_id == current_company.id).first()
        
        if not vehicle or vehicle.status != models.VehicleStatus.AVAILABLE:
            raise HTTPException(status_code=400, detail="Vehicle is not available.")
        if not driver or driver.status != models.DriverStatus.AVAILABLE:
            raise HTTPException(status_code=400, detail="Driver is not available.")
            
        # Update their statuses
        vehicle.status = models.VehicleStatus.ASSIGNED
        driver.status = models.DriverStatus.ASSIGNED

    new_order = models.Order(**order.dict(), status=status, company_id=current_company.id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    create_notification(db, current_company.id, f"Order #{new_order.id} created for {new_order.customer_name}.", "info")
    return new_order

@router.get("/", response_model=List[schemas.OrderOut])
def get_orders(
    status: Optional[str] = Query(None),
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    query = db.query(models.Order).filter(models.Order.company_id == current_company.id)
    if status:
        query = query.filter(models.Order.status == status)
    return query.all()

@router.put("/{order_id}/status", response_model=schemas.OrderOut)
def update_order_status(
    order_id: int,
    status_update: schemas.OrderUpdate,
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    order = db.query(models.Order).filter(
        models.Order.id == order_id, 
        models.Order.company_id == current_company.id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    old_status = order.status
    new_status = status_update.status
    
    if old_status == new_status:
        return order
        
    order.status = new_status
    
    # Handle Data Cascading for Vehicle & Driver
    vehicle = None
    driver = None
    if order.vehicle_id:
        vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == order.vehicle_id).first()
    if order.driver_id:
        driver = db.query(models.Driver).filter(models.Driver.id == order.driver_id).first()
        
    if new_status == models.OrderStatus.IN_TRANSIT:
        if vehicle: vehicle.status = models.VehicleStatus.ON_TRIP
        if driver: driver.status = models.DriverStatus.ON_TRIP
        create_notification(db, current_company.id, f"Order #{order.id} is now In Transit.", "warning")
        
    elif new_status == models.OrderStatus.DELIVERED:
        if vehicle: vehicle.status = models.VehicleStatus.AVAILABLE
        if driver: driver.status = models.DriverStatus.AVAILABLE
        create_notification(db, current_company.id, f"Order #{order.id} has been Delivered!", "success")
        
        # Spawn TripHistory record
        trip = models.TripHistory(
            company_id=current_company.id,
            order_id=order.id,
            vehicle_id=order.vehicle_id,
            driver_id=order.driver_id,
            distance=150.0, # Simulated distance for MVP
            fuel_used=25.0, # Simulated fuel used for MVP
            start_time=order.created_at,
            end_time=datetime.utcnow()
        )
        db.add(trip)
        
    db.commit()
    db.refresh(order)
    return order
