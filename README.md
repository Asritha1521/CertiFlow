# CertiFlow — Bulk Certificate Generation API

CertiFlow is a Python-based REST API that generates participation certificates in bulk from a list of recipients. It validates recipient information, generates individual PDF certificates, tracks each certificate's status, and provides endpoints to retrieve job details and download generated certificates.

## Features

- Create bulk certificate generation jobs.
- Validate recipient names and email addresses.
- Generate personalized PDF certificates using ReportLab.
- Store job and certificate information in a SQLite database.
- Track successful and failed certificate generations.
- Continue processing other recipients if an individual certificate fails.
- Retrieve job status and individual certificate details.
- Download generated certificates as PDF files.
- Interactive API documentation using Swagger UI.
- Automated API tests using Pytest.

## Technology Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **PDF generation:** ReportLab
- **Testing:** Pytest and FastAPI TestClient

## Project Structure

```text
CertiFlow/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── certificates.py
│   └── services/
│       ├── __init__.py
│       └── generator.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── templates/
├── generated/
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/certiflow.git
cd certiflow
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows Command Prompt:

```bat
venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive Swagger documentation:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check whether the API is running |
| POST | `/api/certificates/jobs` | Create a bulk certificate job |
| GET | `/api/certificates/jobs/{job_id}` | Retrieve job status and generation counts |
| GET | `/api/certificates/{certificate_id}` | Retrieve individual certificate details |
| GET | `/api/certificates/{certificate_id}/download` | Download a certificate PDF |

## Example Request

Send a POST request to `/api/certificates/jobs` with the following JSON body:

```json
{
  "event_name": "AI Innovation Workshop",
  "recipients": [
    {
      "name": "Asritha",
      "email": "asritha@example.com"
    },
    {
      "name": "Rahul",
      "email": "rahul@example.com"
    },
    {
      "name": "Priya",
      "email": "priya@example.com"
    }
  ]
}
```

A successful response contains the job ID, event name, total recipients, successful generations, failed generations, and overall status.

Example:

```json
{
  "job_id": 6,
  "event_name": "AI Innovation Workshop",
  "total_certificates": 3,
  "successful": 3,
  "failed": 0,
  "status": "completed"
}
```

The actual job ID will depend on the database.

## Testing

Run the automated tests from the project root:

```bash
python -m pytest -v
```

The tests currently cover the home endpoint, successful bulk job creation, invalid email validation, and retrieval of a nonexistent job.

## Design Decisions

- **FastAPI** provides REST endpoints and automatically generates interactive API documentation.
- **Pydantic** validates request data before certificate processing begins.
- **SQLAlchemy and SQLite** store job and recipient-level certificate information.
- **ReportLab** generates personalized PDF files.
- Each recipient is processed separately so an individual generation error can be recorded without intentionally stopping the remaining recipients.
- The current implementation processes recipients synchronously, making it suitable as a simple assignment implementation rather than a large-scale asynchronous job-processing system.

## Limitations and Future Improvements

- Add background processing for very large jobs.
- Add pagination and more detailed progress reporting.
- Introduce authentication and authorization.
- Add configurable certificate templates.
- Improve automated testing for individual generation failures and PDF retrieval.
- Add production database configuration and deployment support.

## License

This project was developed as a software engineering internship assignment.
