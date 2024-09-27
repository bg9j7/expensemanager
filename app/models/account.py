from app.models import db
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship



class History(db.Model):
    __tablename__ = "history"
    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(Integer,ForeignKey("account.account_number", name="fk_history_account_id"))
    account: Mapped["Account"] = relationship(back_populates="history")
    amount_change: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self):
        return "<History %r>" % self.amount


class Account(db.Model):
    __tablename__ = "account"
    name: Mapped[str] = mapped_column(String(50))
    account_number: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    balance: Mapped[int] = mapped_column(Integer, default=0)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    history: Mapped[list["History"]] = relationship( back_populates="account")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", name="fk_account_user_id"))
    user: Mapped["User"] = relationship(back_populates="accounts")
    def __repr__(self):
        return "<Account %r>" % self.name

    def add(self, amount: int, comment:str="balance added") -> None:
        """
        Adds the given amount to the account balance.

        Args:
            amount (int): The amount to add to the balance.

        Returns:
            None
        """
        self.balance += amount
        history_record = History(account_id=self.account_number, amount_change=amount, comment=comment)
        db.session.add(history_record)
        db.session.commit()

    def deduct_balance(self, amount: int, comment:str="balance deducted") -> None:
        """
        Deducts the given amount from the account balance.

        Args:
            amount (int): The amount to deduct from the balance.

        Returns:
            None
        """
        if self.user_id is None:
            raise ValueError("Account has no user")
        self.balance -= amount
        history_record = History(account_id=self.account_number, amount_change=amount, comment=comment)
        db.session.add(history_record)
        db.session.commit()
