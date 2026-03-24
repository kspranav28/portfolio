from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import os

# --- Database ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./portfolio.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ContactDB(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    subject = Column(String)
    message = Column(Text)

Base.metadata.create_all(bind=engine)

# --- Pydantic Schemas ---
class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    subject: str
    message: str

class ContactResponse(ContactCreate):
    id: int

    class Config:
        from_attributes = True # for pydantic v2

# --- FastAPI App ---
app = FastAPI(title="Portfolio Contact API")

# Setup CORS to allow the frontend to access the API endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Since you serve frontend from a folder or another server, we allow all for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contacts/", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = ContactDB(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contacts/", response_model=list[ContactResponse])
def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = db.query(ContactDB).offset(skip).limit(limit).all()
    return contacts
