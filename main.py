from fastapi import FastAPI, Depends, HTTPException
from api.schemas import TargetCreate, TargetResponse
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Target
import datetime

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/targets", response_model=TargetResponse)
def create_target(target: TargetCreate, db: Session = Depends(get_db)):
    new_target = Target(url=str(target.url),
                        check_interval_seconds=target.check_interval_seconds)
    db.add(new_target)
    db.commit()
    db.refresh(new_target)
    return new_target


@app.get("/api/targets", response_model=list[TargetResponse])
def get_all_targets(db: Session = Depends(get_db)):
    targets = db.query(Target).all()
    return targets


@app.delete("/api/targets/{target_id}", response_model=dict)
def delete_target(target_id: int, db: Session = Depends(get_db)):
    target_obj = db.query(Target).filter(Target.id == target_id).first()
    if target_obj is None:
        raise HTTPException(status_code=404, detail="Target not found.")
    db.delete(target_obj)
    db.commit()
    return {"message": "Target successfully deleted"}
