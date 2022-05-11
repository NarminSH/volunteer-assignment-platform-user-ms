from typing import List
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from users import models
from users.database import engine, SessionLocal
from users.crud import get_user, filter_users, get_users
from pydantic import BaseModel

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


class User(BaseModel):
    field: str
    operator: str
    value: str

class UserList(BaseModel):
    users: List[User]

@app.post('/filter-volunteers/')
def filter_volunteers(data: UserList, db: Session = Depends(get_db)):
    matched_users = []
    print(data.users, 'query over here..........')
    for i in data.users: 
        print(i, 'iiiii')
        print(i.field)
        field = i.field
        operator = i.operator
        value = i.value
        print(type(value), 'value type')
        print(field, 'field', operator, 'operator', value, 'value')
        user = filter_users(db, field=field, operator=operator, value=value)
        if user not in matched_users:
            matched_users.append(user)
            print(matched_users, "all matching users")
    return matched_users


# [
# {
# field: "name",
# operator: "=",
# value: "Musa",
# },
# {
# field: "age",
# operator: ">",
# value: "22",
# },
# {
# field: "location",
# operator: "contains",
# value: "B",
# }
# ]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)