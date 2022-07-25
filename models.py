from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

from database import Base


class User(Base):
    """
    SQLAlchemy User Model
    """
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(50), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        return f"<User {self.username}>"

class Order(Base):
    """
    SQLAlchemy Pizza Order Model
    """
    ORDER_STATUSES = (
        ('PENDING', 'Pending'),
        ('IN-TRANSIT', 'In-Transit'),
        ('DELIVERED', 'Delivered')
    )

    PIZZA_SIZES = (
        ('SMALL', 'Small'),
        ('MEDIUM', 'Medium'),
        ('LARGE', 'Large'),
        ('EXTRA-LARGE', 'Extra-Large')
    )

    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUSES), default="PENDING")
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES), default="SMALL")
    user_id = Column(Integer, ForeignKey('User.id'))

    user = relationship('User', back_populates='orders')

    def __repr__(self):
        return f"<Order {self.id}>"
