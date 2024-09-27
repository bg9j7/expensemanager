from app.models import db
from datetime import date
from sqlalchemy import Integer, String, ForeignKey, DateTime,Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Purchase(db.Model):
    __tablename__ = "purchase"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[date] = mapped_column(Date, default=date.today())
    items: Mapped[list["Items"]] = relationship( back_populates="purchase")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", name="fk_purchase_user_id"))
    user: Mapped["User"] = relationship(back_populates="purchases")
   
    def __repr__(self):
        return "<Purchase %r>" % self.name
    
    @property
    def total_price(self):
        return sum(item.price for item in self.items)

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items)
    @property
    def average_price(self):
        return self.total_price / self.total_quantity
    @property
    def max_price(self):
        return max(item.price for item in self.items)
    @property
    def min_price(self):
        return min(item.price for item in self.items)

class Items(db.Model):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)   
    name: Mapped[str] = mapped_column(String(50))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    purchase_date: Mapped[date] = mapped_column(Date, default=date.today())
    purchase_location: Mapped[str] = mapped_column(String(50))
    purchase_id: Mapped[int] = mapped_column(Integer, ForeignKey("purchase.id", name="fk_items_purchase_id"))
    purchase: Mapped["Purchase"] = relationship(back_populates="items")
    comment: Mapped[str] = mapped_column(String(50), nullable=True)
    item_category_id: Mapped[int] = mapped_column(Integer, ForeignKey("item_category.id", name="fk_items_item_category_id"))
    item_category: Mapped["ItemCategory"] = relationship(back_populates="items")
    
    def __repr__(self):
        return "<Items %r>" % self.name 

class ItemCategory(db.Model):
    __tablename__ = "item_category"

    id: Mapped[int] = mapped_column(primary_key=True)   
    comment: Mapped[str] = mapped_column(String(50), nullable=True)
    items: Mapped[list["Items"]] = relationship( back_populates="item_category")
    def __repr__(self):
        return "<ItemCategory %r>" % self.name