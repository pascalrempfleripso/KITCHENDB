from typing import Optional

import bcrypt
import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return f"<User {self.username}>"


def create_user(username: str, email: str, password: str) -> User:
    salt = bcrypt.gensalt()
    new_user = User(username, email, bcrypt.hashpw(password.encode(), salt))
    #    new_user = User(username=data["username"], email=data["email"], password_hash=bcrypt.hashpw(data["password"].encode(), salt))
    db.session.add(new_user)
    db.session.commit()
    return new_user
