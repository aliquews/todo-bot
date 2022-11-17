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

    def distr(self):
        lst = None
        with Session(self.engine) as session:
            usr_id = select(User.tgid)
            lst = session.scalars(usr_id)
        return lst

    def inline_list(self, id: int):
        lst = None
        with Session(self.engine) as session:
            usrid = session.scalar(self.__select_id_by_tgid(id))
            stmt = select(Tasks.task).where(Tasks.user_id == usrid)
            lst = session.scalars(stmt)
        return lst

    def del_task_db(self, id, text):
        with Session(self.engine) as session:
            usrid = session.scalar(self.__select_id_by_tgid(id))
            stmt = session.get(Tasks, session.scalar(select(Tasks.id).where(Tasks.task == text).where(Tasks.user_id == usrid)))
            session.delete(stmt)
            session.commit()

    def select_task(self, id):
        stmt = None
        with Session(self.engine) as session:
            usr_id = session.scalar(self.__select_id_by_tgid(id))
            stmt = session.scalars(select(Tasks.task).where(Tasks.user_id == usr_id))

        return stmt

    def tasks_dl(self, id): # misc function an outgoing message informing about deadlines
        outdata = dict()
        with Session(self.engine) as session:
            usr_id = select(User.id).where(User.tgid == id)
            stmt = select(Tasks).where(Tasks.user_id == usr_id)
            for task in session.scalars(stmt):
                outdata[task.task] = str(task.deadline).split('-')
        return outdata

db = DataBase(DB_LOGIN)
