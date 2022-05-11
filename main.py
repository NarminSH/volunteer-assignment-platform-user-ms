from sqlalchemy import inspect
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from users import models
from users.database import engine, SessionLocal
from users.crud import get_user, filter_users, get_users
from users import schemas

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/volunteers')
def read_volunteers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.get('/volunteers/{user_id}')
def read_volunteer(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    return user    





@app.post('/filter-volunteers')
def filter_volunteers(data: schemas.UserList, db: Session = Depends(get_db)):
    matched_users = []
    print(data.users, 'query over here..........')
    for i in data.users: 
        field = i.field
        operator = i.operator
        value = i.value
        print(field, 'field', operator, 'operator', value, 'value')
        user = filter_users(db, field=field, operator=operator, value=value)
        if user not in matched_users:
            matched_users.append(user)
            print(matched_users, "all matching users")
    return matched_users


@app.get('/volunteer-fields')
def read_fields():
    columns = [column.name for column in inspect(models.Volunteers).c]
    return columns


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)