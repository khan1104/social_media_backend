
from sqlalchemy import Column,Boolean,TIMESTAMP,text

class TimestampMixin:
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))