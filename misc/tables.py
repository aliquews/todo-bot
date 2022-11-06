from sqlalchemy import Column, ForeignKey, String, Text, create_engine, BigInteger
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import select, exists, delete

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

    def __repr__(self) -> str:
        return f"Tasks(id={self.id},user_id={self.tgid}, task={self.task})"

if __name__ == "__main__":
    #Base.metadata.create_all(engine)
    session = Session(engine)
    usr_id = session.scalar(select(User.id).where(User.tgid == message.from_user.id))
    stmt = session.get(Tasks, session.scalar(select(Tasks.id).where(Tasks.task == text).where(Tasks.user_id == usr_id)))
    session.delete(stmt)
    session.commit()
    session.close()
