from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://rujaajmekrjdhl:235d76e58f29e1a531d66a2ea54040744803287fad1051041108669ed6edc821@ec2-52-3-200-138.compute-1.amazonaws.com/dktkert4drefj"

 ## "postgresql://narmin:narmin123@localhost/vapdb"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()


## MAKE THIS IMPORTANT CHANGE TO USE AUTOCOMMIT TRANSACTIONS WITH BIT.IO
## eng=create_engine('YOUR_POSTRES_CONNECT_STRING', isolation_level="AUTOCOMMIT")