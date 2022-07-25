from database import Base, engine
from models import Order, User

Base.metadata.create_all(bind=engine)
