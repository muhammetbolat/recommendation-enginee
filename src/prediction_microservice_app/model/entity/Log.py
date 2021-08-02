from sqlalchemy import Column, String, DateTime, Integer
from infrastructor.IocManager import IocManager


class Log(IocManager.Base):
    __tablename__ = "log"
    __table_args__ = {"schema": "ai_recommendation"}
    id = Column(Integer, primary_key=True)
    level = Column(String(4000), index=False, unique=False, nullable=False)
    message = Column(String(4000), index=False, unique=False, nullable=True)
    logDatetime = Column(DateTime, index=False, unique=False, nullable=True)

    def __init__(self,
                 level: str = None,
                 logDatetime: str = None,
                 message: str = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = level
        self.message = message
        self.logDatetime = logDatetime
