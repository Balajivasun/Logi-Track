from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter(prefix="/api/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    company_id: int
    message: str

@router.post("/register", response_model=schemas.CompanyOut)
def register_company(company: schemas.CompanyCreate, db: Session = Depends(database.get_db)):
    db_company = db.query(models.Company).filter(models.Company.email == company.email).first()
    if db_company:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_company = models.Company(
        name=company.name,
        email=company.email,
        password=company.password, # Plain text for V1
        contact_number=company.contact_number
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    
    return new_company

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(database.get_db)):
    company = db.query(models.Company).filter(
        models.Company.email == login_data.email,
        models.Company.password == login_data.password
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    return {"company_id": company.id, "message": "Login successful"}
