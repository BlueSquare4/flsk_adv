from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

db_connectioon_string = 'mysql+pymysql://tiy7ihaeprjj94ll4b2x:pscale_pw_KRhnputpIxr8AmX7NIfKM0Xr27ShEj4qgJtSVI3tbKj@aws.connect.psdb.cloud/aj_db?charset=utf8mb4'

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=30), nullable=False, unique=True)
    email_address = Column(String(length=255), nullable=False)
    password_hash = Column(String(length=60), nullable=False)

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(2500))
    status = Column(Boolean, default=True)
    
    
   
    

engine = create_engine(db_connectioon_string,connect_args=
                       {
                           "ssl": {
                                "ssl_ca": "/etc/ssl/cert.pem"
                           }
                       })

def load_todos_from_db():
    with engine.connect() as conn:
     result = conn.execute(text("select * from todos"))
     tasks = []
    for task in result.mappings():
        tasks.append(dict(task))
    return tasks
'''       
def load_todo_from_db(id):
   with engine.connect() as conn:
      result = conn.execute(text(f"select * from todos where id = :val"), val=id)
      rows = result.all()
      if len(rows) == 0:
         return None
      else:
         return dict(rows[0])
'''