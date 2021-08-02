from sqlalchemy import Column, String, Integer
from infrastructor.IocManager import IocManager


class AllData(IocManager.Base):
    __tablename__ = "all_data"
    __table_args__ = {"schema": "ai_recommendation"}

    productId = Column(String(1000), index=True, primary_key=True, unique=True, nullable=False)
    brand = Column(String(1000), index=True, primary_key=True, unique=True, nullable=False)
    numberOfCart = Column(Integer, index=False, unique=False, nullable=False)
    passedDay = Column(Integer, index=False, unique=False, nullable=True)
    category = Column(String(1000), index=False, unique=False, nullable=False)
    subcategory = Column(String(1000), index=False, unique=False, nullable=False)
    name = Column(String(4000), index=False, unique=False, nullable=False)

    def __init__(self,
                 productId: str = None,
                 brand: str = None,
                 numberOfCart: int = None,
                 passedDay: int = None,
                 category: str = None,
                 subcategory: str = None,
                 name: str = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.productId = productId
        self.brand = brand
        self.numberOfCart = numberOfCart
        self.passedDay = passedDay
        self.category = category
        self.subcategory = subcategory
        self.name = name

    def to_dict(self):
        return {
            'productId': self.productId,
            'brand': self.brand,
            'numberOfCart': self.numberOfCart,
            'passedDay': self.passedDay,
            'category': self.category,
            'subcategory': self.subcategory,
            'name': self.name
        }
