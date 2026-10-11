
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class CertificateJob(Base):
    __tablename__ = "certificate_jobs"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(200), nullable=False)
    total_certificates = Column(Integer, default=0)
    successful = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    status = Column(String(30), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    certificates = relationship(
        "Certificate",
        back_populates="job",
        cascade="all, delete-orphan"
    )


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(
        Integer,
        ForeignKey("certificate_jobs.id"),
        nullable=False
    )
    recipient_name = Column(String(200), nullable=False)
    recipient_email = Column(String(200), nullable=False)
    status = Column(String(30), default="pending")
    file_path = Column(String(500), nullable=True)
    error_message = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship(
        "CertificateJob",
        back_populates="certificates"
    )
