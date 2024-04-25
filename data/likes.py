import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Likes(SqlAlchemyBase):
    __tablename__ = 'likes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    recipe_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("recipes.id"))
    recipes = orm.relationship('Recipes', back_populates='likes')
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    users = orm.relationship('User', back_populates='likes')
