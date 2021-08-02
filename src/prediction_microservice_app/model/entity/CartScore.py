from sqlalchemy import Column, String, Float
from infrastructor.IocManager import IocManager


class CartScore(IocManager.Base):
    __tablename__ = "cart_score"
    __table_args__ = {"schema": "ai_recommendation"}

    productId = Column(String(1000), index=True, primary_key=True, unique=True, nullable=False)
    score = Column(Float, index=False, unique=False, nullable=False)

    def __init__(self,
                 productId: str = None,
                 score: float = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.productId = productId
        self.score = score

    def to_json(self):
        return {
            'productId': self.productId,
            'score': self.score
        }