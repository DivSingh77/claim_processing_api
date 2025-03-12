import datetime

from sqlalchemy import TIMESTAMP, Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./claims.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    payer = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    procedure_codes = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

