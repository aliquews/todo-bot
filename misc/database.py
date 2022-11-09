from misc.tables import engine, Base

class DataBase:
    def __init__(self):
        self.engine = engine
        Base.metadata.create_all(self.engine)
