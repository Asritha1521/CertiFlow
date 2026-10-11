
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List


class RecipientInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr


class CertificateJobCreate(BaseModel):
    event_name: str = Field(..., min_length=1, max_length=200)
    recipients: List[RecipientInput] = Field(..., min_length=1)


class CertificateResponse(BaseModel):
    id: int
    recipient_name: str
    recipient_email: str
    status: str
    file_path: str | None = None
    error_message: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CertificateJobResponse(BaseModel):
    id: int
    event_name: str
    total_certificates: int
    successful: int
    failed: int
    status: str

    model_config = ConfigDict(from_attributes=True)
