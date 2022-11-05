from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///test.db', echo=True)
base = declarative_base()

class User(base):
    __tablename__='users'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    def __repr__(self):
        return f'<User(name={self.name})>'

base.metadata.create_all(engine)
