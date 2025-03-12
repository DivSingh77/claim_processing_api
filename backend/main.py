from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from backend.auth import verify_jwt_token
from backend.logging_config import logger
from backend.metrics import REQUEST_COUNT
from backend.models import Base, Claim, SessionLocal, engine

app = FastAPI()

# Initialize the database
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.post("/claims")
def submit_claim(payer: str, amount: float, procedure_codes: str, db: Session = Depends(get_db)):
    REQUEST_COUNT.inc()
    logger.info(f"Submitting claim: payer={payer}, amount={amount}, procedure_codes={procedure_codes}")
    claim = Claim(payer=payer, amount=amount, procedure_codes=procedure_codes)
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim

@app.get("/claims/{id}")
def get_claim(id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim

@app.get("/claims/status/{id}")
def check_claim_status(id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return {"id": claim.id, "status": claim.status}