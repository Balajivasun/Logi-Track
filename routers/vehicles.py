from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models, schemas, dependencies, database

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])

def create_notification(db: Session, company_id: int, message: str, type: str):
    notif = models.Notification(company_id=company_id, message=message, type=type)
    db.add(notif)
    db.commit()

@router.post("/", response_model=schemas.VehicleOut)
def create_vehicle(
    vehicle: schemas.VehicleCreate,
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    new_vehicle = models.Vehicle(**vehicle.dict(), company_id=current_company.id)
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    
    create_notification(db, current_company.id, f"New vehicle {new_vehicle.vehicle_number} added.", "success")
    return new_vehicle

@router.get("/", response_model=List[schemas.VehicleOut])
def get_vehicles(
    status: Optional[str] = Query(None),
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    query = db.query(models.Vehicle).filter(models.Vehicle.company_id == current_company.id)
    if status:
        query = query.filter(models.Vehicle.status == status)
    return query.all()

@router.get("/{vehicle_id}", response_model=schemas.VehicleOut)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == vehicle_id, 
        models.Vehicle.company_id == current_company.id
    ).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.put("/{vehicle_id}", response_model=schemas.VehicleOut)
def update_vehicle(
    vehicle_id: int,
    vehicle_update: schemas.VehicleUpdate,
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == vehicle_id, 
        models.Vehicle.company_id == current_company.id
    ).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    update_data = vehicle_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vehicle, key, value)
        
    db.commit()
    db.refresh(vehicle)
    return vehicle

@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == vehicle_id, 
        models.Vehicle.company_id == current_company.id
    ).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Optional: check if on trip before delete
    if vehicle.status in [models.VehicleStatus.ON_TRIP, models.VehicleStatus.ASSIGNED]:
        raise HTTPException(status_code=400, detail="Cannot delete a vehicle that is assigned or on a trip.")
        
    db.delete(vehicle)
    db.commit()
    create_notification(db, current_company.id, f"Vehicle {vehicle.vehicle_number} removed.", "warning")
    return {"message": "Vehicle deleted successfully"}
