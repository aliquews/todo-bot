from sqlalchemy import Column, ForeignKey, Text, BigInteger, Date, create_engine
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()
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
