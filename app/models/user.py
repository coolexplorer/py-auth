from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime
from databases.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=True)
    hashed_password = Column(String)
    create_date = Column(DateTime, default=datetime.utcnow())
    last_login = Column(DateTime, default=datetime.utcnow())

