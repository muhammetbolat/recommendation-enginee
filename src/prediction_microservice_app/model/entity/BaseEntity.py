from datetime import datetime
from sqlalchemy import Integer, DateTime, TIMESTAMP, text, Column, String
from sqlalchemy.ext.declarative import declared_attr


class Entity:
    id = Column(
        Integer,
        primary_key=True
    )

