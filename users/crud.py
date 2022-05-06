from sqlalchemy.orm import Session
from . import models


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Volunteers).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.Volunteers).filter(models.Volunteers.id == user_id).first()