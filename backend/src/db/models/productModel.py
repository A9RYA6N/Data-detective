from sqlalchemy import Column, String, Text, Integer, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime

from src.config.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(
        UUID(as_uuid=True),
        primary_key = True,
        default = uuid.uuid4
    )
    source = Column(String, nullable=False)
    product_identifier = Column(String, nullable=False)
    product_url = Column(String, nullable=False)
    name = Column(Text)
    currency = Column(String)
    price = Column(Numeric(10, 2))
    mrp = Column(Numeric(10, 2))
    discount_percentage = Column(Numeric(5, 2))
    review_score = Column(Numeric(2, 1))
    review_count = Column(Integer)
    seller_company = Column(Text)
    misc_details = Column(JSONB)
    created_at = Column(
        DateTime,
        default = datetime.now
    ) 
    updated_at = Column(
        DateTime,
        default = datetime.now
    )
    deleted_at = Column(
        DateTime,
        nullable = True
    )