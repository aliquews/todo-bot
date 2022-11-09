from db.tables import Base, User, Tasks
from sqlalchemy import create_engine, exists, select, update
from sqlalchemy.orm import Session
from config import DB_LOGIN

class DataBase:
    def __init__(self, db_login: str):
        self.engine = create_engine(db_login)
        Base.metadata.create_all(self.engine)

    def user_add_to_db(self, usr_id: int):
        with Session(self.engine) as session:
            if session.query(exists().where(User.tgid == usr_id)).scalar() == False:
                user = User(
                    tgid=usr_id
                )
                session.add_all([user])
                session.commit()

    def __select_id_by_tgid(self, tgid: int):
        return select(User.id).where(User.tgid == tgid)

    def task_add_to_db(self, text: str, tgid: int):
        with Session(self.engine) as session:
            tsk = Tasks(
                task=text,
                user_id=session.scalar(self.__select_id_by_tgid(tgid))
            )
            session.add_all([tsk])
            session.commit()

    def add_deadline(self, txt, sqldate):
        with Session(self.engine) as session:
            session.execute(
                update(Tasks)
                .where(Tasks.task == txt[0])
                .values(deadline=sqldate)
            )
            session.commit()

db = DataBase(DB_LOGIN)
