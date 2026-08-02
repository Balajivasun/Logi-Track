from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas, dependencies, database

router = APIRouter(prefix="/api/company", tags=["company"])

@router.get("/profile", response_model=schemas.CompanyOut)
def get_company_profile(current_company: models.Company = Depends(dependencies.get_current_company)):
    return current_company

@router.put("/profile", response_model=schemas.CompanyOut)
def update_company_profile(
    company_update: schemas.CompanyUpdate,
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    update_data = company_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_company, key, value)
        
    db.commit()
    db.refresh(current_company)
    return current_company

@router.get("/dashboard")
def get_dashboard_metrics(
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    cid = current_company.id
    
    total_vehicles = db.query(models.Vehicle).filter(models.Vehicle.company_id == cid).count()
    vehicles_available = db.query(models.Vehicle).filter(models.Vehicle.company_id == cid, models.Vehicle.status == models.VehicleStatus.AVAILABLE).count()
    vehicles_on_trip = db.query(models.Vehicle).filter(models.Vehicle.company_id == cid, models.Vehicle.status == models.VehicleStatus.ON_TRIP).count()
    
    total_drivers = db.query(models.Driver).filter(models.Driver.company_id == cid).count()
    drivers_available = db.query(models.Driver).filter(models.Driver.company_id == cid, models.Driver.status == models.DriverStatus.AVAILABLE).count()
    
    active_orders = db.query(models.Order).filter(
        models.Order.company_id == cid, 
        models.Order.status != models.OrderStatus.DELIVERED,
        models.Order.status != models.OrderStatus.CANCELLED
    ).count()
    
    total_orders = db.query(models.Order).filter(models.Order.company_id == cid).count()
    completed_trips = db.query(models.TripHistory).filter(models.TripHistory.company_id == cid).count()
    
    return {
        "total_vehicles": total_vehicles,
        "vehicles_available": vehicles_available,
        "vehicles_on_trip": vehicles_on_trip,
        "total_drivers": total_drivers,
        "drivers_available": drivers_available,
        "active_orders": active_orders,
        "total_orders": total_orders,
        "completed_trips": completed_trips
    }
