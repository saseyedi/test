from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime, event, Boolean
from sqlalchemy_utils import PasswordType, UUIDType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from models.settings import DB_URL, PASSWORD_SCHEMES
from datetime import datetime


db = create_engine(DB_URL)
base = declarative_base()


class User(base):
    __tablename__ = 'users'

    id = Column(UUIDType(binary=False), primary_key=True)
    user_name = Column('user_name', String, nullable = False, unique = True)
    password = Column('password', PasswordType, PasswordType(
            # The returned dictionary is forwarded to the CryptContext
            onload = lambda **kwargs: dict(
                schemes = PASSWORD_SCHEMES,
                **kwargs
            )), unique = False, nullable = False)

class Category(base):
    __tablename__ = 'categories'

    id = Column(UUIDType(binary=False), primary_key=True)
    task_type = Column('task_type', String, nullable = False)


class Task(base):
    __tablename__= 'tasks'

    id = Column(UUIDType(binary=False), primary_key=True)
    type_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    task_name = Column('task_name', String, nullable = False)
    creation_date = Column('creation_date', DateTime, nullable = False, default = datetime.now())
    update_date = Column('update_date', DateTime, nullable = False, default = datetime.now())

    category = relationship("Category", back_populates = "categories")
    user = relationship("User", back_populates = "users")    


@event.listens_for(Task, 'after_update')
def update_time():
    Task.update_date = datetime.now()


if __name__ == '__main__':
    Session=sessionmaker(db)
    session=Session()
    base.metadata.create_all(db)
