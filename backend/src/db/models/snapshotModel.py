from sqlalchemy import Column, ForeignKey, Numeric, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from src.config.db import Base

class Snapshot(Base):
    __tablename__="snapshot"

    id = Column(
        UUID(as_uuid=True),
        primary_key = True,
        default = uuid.uuid4
    )
    product_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("products.id"),
        nullable=False
    )
    price = Column(Numeric(10, 2))
    mrp = Column(Numeric(10, 2))
    review_score = Column(Numeric(2, 1))
    review_count = Column(Integer)
    discount_percentage = Column(Numeric(5, 2))
    scraped_at = Column(DateTime, default=datetime.now)