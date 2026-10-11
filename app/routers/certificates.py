
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CertificateJob, Certificate
from app.schemas import CertificateJobCreate
from app.services.generator import generate_certificate


router = APIRouter(
    prefix="/api/certificates",
    tags=["Certificates"]
)


@router.post("/jobs")
def create_certificate_job(
    request: CertificateJobCreate,
    db: Session = Depends(get_db)
):
    job = CertificateJob(
        event_name=request.event_name,
        total_certificates=len(request.recipients),
        status="processing"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient in request.recipients:
        certificate = Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            status="pending"
        )

        db.add(certificate)
        db.commit()
        db.refresh(certificate)

        try:
            file_path = generate_certificate(
                recipient_name=recipient.name,
                event_name=request.event_name,
                certificate_id=certificate.id
            )

            certificate.file_path = str(file_path)
            certificate.status = "completed"
            job.successful += 1

        except Exception as error:
            certificate.status = "failed"
            certificate.error_message = str(error)[:500]
            job.failed += 1

        db.commit()

    job.status = "completed"
    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "total_certificates": job.total_certificates,
        "successful": job.successful,
        "failed": job.failed,
        "status": job.status
    }


@router.get("/jobs/{job_id}")
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(CertificateJob).filter(
        CertificateJob.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "total_certificates": job.total_certificates,
        "successful": job.successful,
        "failed": job.failed,
        "status": job.status
    }


@router.get("/{certificate_id}")
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = db.query(Certificate).filter(
        Certificate.id == certificate_id
    ).first()

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    return {
        "id": certificate.id,
        "job_id": certificate.job_id,
        "recipient_name": certificate.recipient_name,
        "recipient_email": certificate.recipient_email,
        "status": certificate.status,
        "file_path": certificate.file_path,
        "error_message": certificate.error_message
    }


@router.get("/{certificate_id}/download")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = db.query(Certificate).filter(
        Certificate.id == certificate_id
    ).first()

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    if not certificate.file_path:
        raise HTTPException(
            status_code=404,
            detail="Certificate file not available"
        )

    file_path = Path(certificate.file_path)

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found on disk"
        )

    return FileResponse(
        path=str(file_path),
        media_type="application/pdf",
        filename=f"certificate_{certificate.id}.pdf"
    )
