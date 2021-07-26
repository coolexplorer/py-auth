from sqlalchemy import Table, Column, Integer, String
from databases.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=True)
    hashed_password = Column(String)
    email = Column(String)

