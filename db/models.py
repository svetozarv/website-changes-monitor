from sqlalchemy import Column, DateTime, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Target(Base):
    __tablename__ = "targets"

    last_checked = Column(DateTime, default=datetime.utcnow)
    last_content_hash = Column(String)

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Target URL to monitor (e.g., https://example.com)
    url = Column(String, unique=True, index=True, nullable=False)

    # Polling interval in seconds
    check_interval_seconds = Column(Integer, default=60)

    # Flag to pause monitoring without deleting the target
    is_active = Column(Boolean, default=True)

    # Timestamp of creation
    created_at = Column(DateTime, default=datetime.utcnow)


class CheckLog(Base):
    __tablename__ = "check_logs"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key linking to the Target table
    target_id = Column(Integer, ForeignKey("targets.id", ondelete="CASCADE"), nullable=False)

    # HTTP status code returned (e.g., 200, 404, 500)
    status_code = Column(Integer, nullable=True)

    content_hash = Column(String, nullable=True)

    # Response time in milliseconds
    response_time_ms = Column(Integer, nullable=True)

    # Timestamp of the check
    checked_at = Column(DateTime, default=datetime.utcnow)
