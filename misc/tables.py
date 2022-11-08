from sqlalchemy import Column, ForeignKey, String, Text, create_engine, BigInteger, Date
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import select, exists, delete
from datetime import datetime

Base = declarative_base()

engine = create_engine("postgresql+psycopg2://postgres:111@localhost/newdb")


class User(Base):
    __tablename__ = "telegram_user"
    id = Column(BigInteger, primary_key=True)
    tgid = Column(BigInteger)
    tasks = relationship("Tasks")

    def __repr__(self) -> str:
        return f"User(id={self.id}, tgid={self.tgid})"

class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("telegram_user.id"))
    task = Column(Text)
    deadline = Column(Date, index=True)

    def __repr__(self) -> str:
        return f"Tasks(id={self.id},user_id={self.user_id}, task={self.task}, deadline={self.deadline})"

if __name__ == "__main__":
    # Base.metadata.create_all(engine)
    session = Session(engine)
    stmt = select(Tasks).where(Tasks.user_id == 1)
    for task in session.scalars(stmt):
        print(task.task, task.deadline)
    session.close()
    print(type((datetime.today() - datetime(2022,11,10)).days))
