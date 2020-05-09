from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URI = 'sqlite:///database.db'

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(DB_URI))
session = scoped_session(Session)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    middlename = Column(String(50))
    companyid = Column(Integer)
    companytitle = Column(String(50))
    jobtype = Column(Integer)
    jobid = Column(Integer)
    jobtitle = Column(String(50))
    isAdviser = Column(Boolean)

    def __init__(self, firstname, lastname, middlename, companyid, companytitle, jobtype, jobid, jobtitle, isAdviser):
        self.firstname = firstname
        self.lastname = lastname
        self.middlename = middlename
        self.companyid = companyid
        self.ccmpanytitle = companytitle
        self.jobtype = jobtype
        self.jobid = jobid
        self.jobtitle = jobtitle
        self.isAdviser = isAdviser

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['firstname', 'lastname', 'middlename', 'companytitle', 'jobtitle', 'isAdviser']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d


if __name__ == "__main__":

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    users = [
        User("Владыка", "Кожемякин", "Олегович", 1, "МТС", 12, 134, "Программист высшего ранга", True)
    ]

    session.add(users[0])
    session.commit()
