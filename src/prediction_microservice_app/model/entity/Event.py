from sqlalchemy import Column, String, Integer, DateTime, Float
from infrastructor.IocManager import IocManager


class Event(IocManager.Base):
    __tablename__ = "event"
    __table_args__ = {"schema": "ai_recommendation"}

    productId = Column(String(1000), index=True, primary_key=True, unique=True, nullable=False)
    numberOfCart = Column(Integer, index=False, unique=False, nullable=False)
    price = Column(Float, index=False, unique=False, nullable=False)
    passedDay = Column(Integer, index=False, unique=False, nullable=True)

    def __init__(self,
                 productId: str = None,
                 numberOfCart: int = None,
                 price: float = None,
                 passedDay: int = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.productId = productId
        self.numberOfCart = numberOfCart
        self.price = price
        self.passedDay = passedDay
