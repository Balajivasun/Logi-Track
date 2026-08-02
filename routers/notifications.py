from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas, dependencies, database

router = APIRouter(prefix="/api/notifications", tags=["notifications"])

@router.get("/", response_model=List[schemas.NotificationOut])
def get_notifications(
    db: Session = Depends(database.get_db),
    current_company: models.Company = Depends(dependencies.get_current_company)
):
    # Get last 10 notifications
    return db.query(models.Notification).filter(
        models.Notification.company_id == current_company.id
    ).order_by(models.Notification.created_at.desc()).limit(10).all()
