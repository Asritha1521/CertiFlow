
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to CertiFlow API"


def test_create_certificate_job():
    response = client.post(
        "/api/certificates/jobs",
        json={
            "event_name": "Testing Workshop",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "testuser@example.com"
                },
                {
                    "name": "Another User",
                    "email": "another@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["total_certificates"] == 2
    assert data["successful"] == 2
    assert data["failed"] == 0
    assert data["status"] == "completed"



def test_invalid_email():
    response = client.post(
        "/api/certificates/jobs",
        json={
            "event_name": "Testing Workshop",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "not-an-email"
                }
            ]
        }
    )

    assert response.status_code == 422


def test_missing_job():
    response = client.get("/api/certificates/jobs/999999")
    assert response.status_code == 404
    
def test_retrieve_certificate_and_download():
    # Create a certificate job
    response = client.post(
        "/api/certificates/jobs",
        json={
            "event_name": "Certificate Testing",
            "recipients": [
                {
                    "name": "Download Test User",
                    "email": "downloadtest@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    # Retrieve the generated certificate using its database ID
    job_id = response.json()["job_id"]

    db_response = client.get(
        f"/api/certificates/jobs/{job_id}"
    )
    assert db_response.status_code == 200
    assert db_response.json()["successful"] == 1

    # Find the certificate ID from the database-backed job
    from app.database import SessionLocal
    from app.models import Certificate

    db = SessionLocal()
    try:
        certificate = (
            db.query(Certificate)
            .filter(Certificate.job_id == job_id)
            .first()
        )
        assert certificate is not None
        certificate_id = certificate.id
    finally:
        db.close()

    # Retrieve certificate details
    detail_response = client.get(
        f"/api/certificates/{certificate_id}"
    )
    assert detail_response.status_code == 200
    assert detail_response.json()["recipient_name"] == "Download Test User"

    # Download the PDF
    download_response = client.get(
        f"/api/certificates/{certificate_id}/download"
    )
    assert download_response.status_code == 200
    assert download_response.headers["content-type"] == "application/pdf"
    assert download_response.content.startswith(b"%PDF")


def test_missing_certificate_download():
    response = client.get(
        "/api/certificates/999999/download"
    )
    assert response.status_code == 404


def test_individual_certificate_failure(monkeypatch):
    from app.routers import certificates as certificate_router

    original_generator = certificate_router.generate_certificate

    def generator_with_failure(
        recipient_name,
        event_name,
        certificate_id
    ):
        if recipient_name == "Fail User":
            raise RuntimeError("Simulated PDF generation failure")

        return original_generator(
            recipient_name,
            event_name,
            certificate_id
        )

    monkeypatch.setattr(
        certificate_router,
        "generate_certificate",
        generator_with_failure
    )

    response = client.post(
        "/api/certificates/jobs",
        json={
            "event_name": "Failure Handling Test",
            "recipients": [
                {
                    "name": "Success User",
                    "email": "success@example.com"
                },
                {
                    "name": "Fail User",
                    "email": "fail@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["total_certificates"] == 2
    assert data["successful"] == 1
    assert data["failed"] == 1
    assert data["status"] == "completed"
