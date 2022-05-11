from sqlalchemy.orm import Session
from . import models


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Volunteers).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.Volunteers).filter(models.Volunteers.id == user_id).first()


def filter_users(db: Session, field, operator, value):
    print(field,operator, value, 'query get user filter func')

    if operator == '=':
        print('operator is =')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, field) == value).first()
    elif operator == '>':
        print('operator is >')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, field) > value).first()
    elif operator == '<':
        print('operator is <')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, field) < value).first()
    elif operator == '>=':
        print('operator is >=')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, field) >= value).first()
    elif operator == '<=':
        print('operator is <=')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, field) <= value).first()
    elif operator == 'contains':
        print('operator is contains')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, field).contains(value)).first()