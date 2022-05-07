import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from users import models
from users.database import engine, SessionLocal
from users.crud import get_user, get_users

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)