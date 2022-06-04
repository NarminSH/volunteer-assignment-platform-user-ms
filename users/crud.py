from sqlalchemy import and_
from sqlalchemy.orm import Session
from . import models

def get_users(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Volunteers).offset(skip).limit(limit).all()


def get_user(db: Session, candidate_id: int):
    return db.query(models.Volunteers).filter(models.Volunteers.candidate_id == candidate_id).first()


def filter_users(db: Session, requirement, operator, value):

    if operator == '=':
        print('operator is =')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, requirement) == value).all()
    elif operator == '>':
        print('operator is >')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, requirement) > value).all()
    elif operator == '<':
        print('operator is <')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, requirement) < value).all()
    elif operator == '>=':
        print('operator is >=')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, requirement) >= value).all()
    elif operator == '<=':
        print('operator is <=')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, requirement) <= value).all()
    elif operator == 'not':
        print('operator is !=')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, requirement) != value).all()
    elif operator == 'contains':
        print('operator is contains')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, requirement).contains(value)).all()

