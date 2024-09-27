
from app.models import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(50))
    authenticated: Mapped[bool] = mapped_column(default=False)

    accounts:Mapped[list["Account"]] = relationship( back_populates="user")
    purchases:Mapped[list["Purchase"]] = relationship( back_populates="user")

    def is_authenticated(self):
        return self.authenticated
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.name
    

        