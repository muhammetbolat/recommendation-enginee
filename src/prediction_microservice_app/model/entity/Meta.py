from sqlalchemy import Column, String
from infrastructor.IocManager import IocManager


class Meta(IocManager.Base):
    __tablename__ = "meta"
    __table_args__ = {"schema": "ai_recommendation"}

    productId = Column(String(1000), index=True, primary_key=True, unique=True, nullable=False)
    brand = Column(String(1000), index=False, unique=False, nullable=False)
    category = Column(String(1000), index=False, unique=False, nullable=False)
    subcategory = Column(String(1000), index=False, unique=False, nullable=False)
    name = Column(String(4000), index=False, unique=False, nullable=False)

    def __init__(self,
                 productId: str = None,
                 brand: str =  None,
                 category: str = None,
                 subcategory: str = None,
                 name: str = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.productId = productId,
        self.brand = brand
        self.category = category
        self.subcategory = subcategory
        self.name = name
