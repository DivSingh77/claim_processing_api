from backend.models import Claim, SessionLocal, init_db
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

app = FastAPI()

# Initialize Database
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/claims")
def submit_claim(payer: str, amount: float, procedure_codes: str, db: Session = Depends(get_db)):
    claim = Claim(payer=payer, amount=amount, procedure_codes=procedure_codes)
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return {"message": "Claim submitted", "claim_id": claim.id}

@app.get("/claims/{id}")
def get_claim(id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim

@app.get("/claims/status/{id}")
def get_claim_status(id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return {"claim_id": claim.id, "status": claim.status}

@app.get("/health")
def health_check():
    return {"status": "OK"}
