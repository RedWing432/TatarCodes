import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    input = sqlalchemy.Column(sqlalchemy.String)
    input_data = sqlalchemy.Column(sqlalchemy.String)
    output = sqlalchemy.Column(sqlalchemy.String)
    output_data = sqlalchemy.Column(sqlalchemy.String)
