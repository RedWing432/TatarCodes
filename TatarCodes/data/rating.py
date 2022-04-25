import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Rating(SqlAlchemyBase):
    __tablename__ = 'rating'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    rank = sqlalchemy.Column(sqlalchemy.String)
    rating = sqlalchemy.Column(sqlalchemy.Integer)

    user = orm.relation("Users", back_populates='rating')

