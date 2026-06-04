from sqlalchemy.orm import Session
from src.db.models.snapshotModel import Snapshot

def createSnapshot(db: Session, data: dict):
    snapshot = Snapshot(**data)
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot