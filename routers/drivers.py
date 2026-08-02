from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models, schemas, dependencies, database

router = APIRouter(prefix="/api/drivers", tags=["drivers"])

def create_notification(db: Session, company_id: int, message: str, type: str):
    notif = models.Notification(company_id=company_id, message=message, type=type)
    db.add(notif)
    db.commit()

@router.post("/", response_model=schemas.DriverOut)
def create_driver(
    driver: schemas.DriverCreate,
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    new_driver = models.Driver(**driver.dict(), company_id=current_company.id)
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    
    create_notification(db, current_company.id, f"New driver {new_driver.name} onboarded.", "success")
    return new_driver

@router.get("/", response_model=List[schemas.DriverOut])
def get_drivers(
    status: Optional[str] = Query(None),
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    query = db.query(models.Driver).filter(models.Driver.company_id == current_company.id)
    if status:
        query = query.filter(models.Driver.status == status)
    return query.all()

@router.get("/{driver_id}", response_model=schemas.DriverOut)
def get_driver(
    driver_id: int,
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    driver = db.query(models.Driver).filter(
        models.Driver.id == driver_id, 
        models.Driver.company_id == current_company.id
    ).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.put("/{driver_id}", response_model=schemas.DriverOut)
def update_driver(
    driver_id: int,
    driver_update: schemas.DriverUpdate,
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    driver = db.query(models.Driver).filter(
        models.Driver.id == driver_id, 
        models.Driver.company_id == current_company.id
    ).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    update_data = driver_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(driver, key, value)
        
    db.commit()
    db.refresh(driver)
    return driver

@router.delete("/{driver_id}")
def delete_driver(
    driver_id: int,
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    driver = db.query(models.Driver).filter(
        models.Driver.id == driver_id, 
        models.Driver.company_id == current_company.id
    ).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    if driver.status in [models.DriverStatus.ON_TRIP, models.DriverStatus.ASSIGNED]:
        raise HTTPException(status_code=400, detail="Cannot delete a driver that is assigned or on a trip.")
        
    db.delete(driver)
    db.commit()
    create_notification(db, current_company.id, f"Driver {driver.name} removed.", "warning")
    return {"message": "Driver deleted successfully"}
