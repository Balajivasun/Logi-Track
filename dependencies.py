from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
import database, models

def get_current_company(company_id: int = Header(..., alias="Company-ID"), db: Session = Depends(database.get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=401, detail="Invalid Company ID")
    return company
