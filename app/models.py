from typing import Optional

import bcrypt
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin

from app import db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Recipe(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(200), index=True)
    author: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)


class Ingredients(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    recipe_id: so.Mapped[int] = so.mapped_column(index=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    amount: so.Mapped[int] = so.mapped_column(sa.Integer(10), index=True)
    unit: so.Mapped[str] = so.mapped_column(sa.String(20), index=True)


class Instruction(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    recipe_id: so.Mapped[int] = so.mapped_column(index=True)
    tasks: so.Mapped[str] = so.mapped_column(sa.String(5000), index=True)


@login.user_loader
def load_user(user_id: int) -> User:
    return db.session.get(User, user_id)


def create_user(username: str, email: str, password: str) -> User:
    salt = bcrypt.gensalt()
    new_user = User(username=username, email=email, password_hash=bcrypt.hashpw(password.encode(), salt))
    db.session.add(new_user)
    db.session.commit()
    return new_user
