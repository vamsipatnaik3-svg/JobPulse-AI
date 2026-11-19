
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Boolean,
    DateTime,
    JSON
)

from app.database.db import Base


class EmailAnalysis(Base):

    __tablename__ = "email_analyses"

    id = Column(Integer, primary_key=True, index=True)

    # Original Gmail information
    gmail_message_id = Column(String, unique=True, nullable=True, index=True)
    sender = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    received_at = Column(String, nullable=True)

    # Rule-based processing information
    job_score = Column(Integer, nullable=True)

    # GenAI classification
    category = Column(String, nullable=True)
    is_job_related = Column(Boolean, nullable=True)
    confidence = Column(Float, nullable=True)

    # GenAI extracted information
    '''Instead of creating a separate database column for every extracted field, we're initially storing the entire dictionary in a JSON column.
    This makes it easier to add new extraction fields later.'''
    extracted_details = Column(JSON, nullable=True)

    # GenAI summary
    summary = Column(Text, nullable=True)

    # Processing information
    processing_status = Column(String, default="PENDING")
    error = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
