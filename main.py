from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import company, vehicles, auth, drivers, orders, notifications

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LOGI-TRACK API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(company.router)
app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(orders.router)
app.include_router(notifications.router)
# Add drivers, orders, trips later as needed for the complete project

# Mount the static files for the frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
