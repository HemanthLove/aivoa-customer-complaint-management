# AI-Powered Customer Complaint Management System

An AI-powered Customer Complaint Management System designed for pharmaceutical manufacturing workflows.

The application helps users process pharmaceutical customer complaints through an AI Copilot. Instead of manually entering complaint information into the complaint form, users can provide a complaint in natural language or upload a complaint PDF. The system extracts relevant complaint information, performs an AI-based risk assessment, and populates the structured complaint form.

The system also supports AI-assisted complaint corrections and an optional Complaint Completeness Checker.

---

## Features

- AI-assisted customer complaint logging
- Natural-language complaint processing
- Automatic extraction of customer information
- Product and product strength extraction
- Batch / lot number extraction
- Manufacturing date extraction
- Expiry date extraction
- Affected quantity and unit extraction
- Complaint description extraction
- Defect type and defect description extraction
- Facility and material impact information
- AI-based severity assessment
- AI-based risk-level assessment
- Recommended next action
- Risk assessment rationale
- AI-assisted complaint editing and correction
- Preservation of unchanged complaint information during edits
- Pharmaceutical complaint PDF extraction
- Complaint persistence using PostgreSQL
- Complaint Completeness Checker
- Completeness score from 0–100
- Present and missing core complaint field detection
- React-based web interface
- Redux state management
- FastAPI REST API
- LangGraph-based AI workflows
- Groq LLM integration
- FastAPI / Swagger API documentation

---

## Technology Stack

### Frontend

- React
- Redux Toolkit
- React Redux
- Vite
- JavaScript
- CSS
- Google Inter font

### Backend

- Python
- FastAPI
- Uvicorn
- LangGraph
- LangChain
- LangChain Groq
- Pydantic
- Pydantic Settings
- SQLAlchemy
- PostgreSQL
- Psycopg

### Document Processing

- PyPDF

### AI

- Groq
- Structured LLM output using Pydantic schemas
- LangGraph workflows

---

## How It Works

The application follows an AI-assisted Customer Complaint workflow.

### 1. Enter a Customer Complaint

The user provides a complaint through the AI Copilot using natural language.

For example:

    Apollo Pharmacy reported discolored amoxicillin capsules 500 mg.

The user does not need to manually populate the complaint form.

---

### 2. AI Complaint Processing

The complaint is sent from the React frontend to the FastAPI backend.

The backend invokes the LangGraph complaint-processing workflow.

The workflow sends the complaint to the configured Groq language model and requests structured complaint information.

The AI extracts information such as:

- Customer name
- Customer source
- Product name
- Product strength
- Batch number
- Manufacturing date
- Expiry date
- Affected quantity
- Quantity unit
- Complaint description
- Facility information
- Material impact
- Defect type
- Defect description

The AI also generates:

- Severity
- Risk level
- Recommended action
- Risk rationale

---

### 3. Populate the Complaint Form

The structured AI response is returned to the frontend.

Redux stores the complaint information and risk assessment.

The complaint form is then populated automatically with the extracted information.

The user can review the structured complaint and AI-generated risk assessment.

---

### 4. AI Risk Assessment

The AI evaluates the complaint information and generates a risk assessment.

The assessment contains:

- Severity
- Risk level
- Recommended action
- Rationale

The risk assessment is displayed alongside the complaint information in the application.

---

### 5. Correct or Edit a Complaint

The user can provide a correction through the AI Copilot.

For example:

    Sorry, the batch number is BMX240603 and affected quantity is 50 capsules.

The edit workflow receives:

- The existing complaint
- The user's correction

The LangGraph edit workflow instructs the AI to:

- Apply only the requested changes
- Preserve unchanged information
- Avoid inventing information
- Return the complete updated complaint
- Reassess the risk assessment when appropriate

The updated complaint is then reflected in the complaint form.

---

### 6. Upload a Complaint PDF

The user can upload a pharmaceutical customer complaint PDF through the AI Copilot.

The backend:

1. Receives the uploaded PDF.
2. Reads the PDF contents using PyPDF.
3. Extracts readable text.
4. Sends the extracted text through the complaint-processing LangGraph workflow.
5. Converts the result into structured complaint information.
6. Generates the risk assessment.
7. Stores the complaint in PostgreSQL.
8. Returns the structured result to the frontend.

The extracted information is then displayed in the complaint form.

---

### 7. Check Complaint Completeness

The optional Complaint Completeness Checker evaluates six core complaint fields:

- Customer Name
- Product Name
- Batch Number
- Defect Type
- Affected Quantity
- Complaint Description

The checker returns:

- Completeness score
- Complete / incomplete status
- Present fields
- Missing fields
- Notes

A complaint is considered complete when all six core fields are present.

---

## Application Flow

    Customer Complaint / PDF
              |
              v
       React + Redux Frontend
              |
              v
          FastAPI API
              |
              v
          LangGraph
              |
              v
          Groq LLM
              |
              v
     Structured Complaint Data
              |
        +-----+-----+
        |           |
        v           v
 Complaint Form   Risk Assessment
        |
        v
   PostgreSQL


For PDF processing:

    PDF Upload
        |
        v
    FastAPI
        |
        v
     PyPDF
        |
        v
   Extracted Text
        |
        v
    LangGraph
        |
        v
     Groq LLM
        |
        v
 Structured Complaint
        |
        +----> Complaint Form
        |
        +----> Risk Assessment
        |
        +----> PostgreSQL

---

## LangGraph Workflows

The backend uses LangGraph to organize the AI processing workflows.

### Complaint Processing Graph

The complaint processing graph receives complaint text and produces a structured `ComplaintAIResult`.

The workflow:

    START
      |
      v
    process_complaint
      |
      v
     END

---

### Complaint Editing Graph

The editing graph receives the current complaint and the user's correction.

The workflow:

    START
      |
      v
    edit_complaint
      |
      v
     END

The AI is instructed to preserve information that was not explicitly changed.

---

### Complaint Completeness Graph

The completeness graph receives the current structured complaint and evaluates the required core fields.

The workflow:

    START
      |
      v
    check_completeness
      |
      v
     END

---

## Project Structure

    AIVOA/
    │
    ├── backend/
    │   └── app/
    │       ├── agents/
    │       │   ├── __init__.py
    │       │   ├── complaint_graph.py
    │       │   ├── completeness_graph.py
    │       │   ├── edit_graph.py
    │       │   └── state.py
    │       │
    │       ├── api/
    │       │   ├── __init__.py
    │       │   └── complaints.py
    │       │
    │       ├── database/
    │       │   ├── __init__.py
    │       │   └── database.py
    │       │
    │       ├── models/
    │       │   ├── __init__.py
    │       │   ├── base.py
    │       │   └── complaint.py
    │       │
    │       ├── schemas/
    │       │   ├── __init__.py
    │       │   ├── complaint.py
    │       │   └── completeness.py
    │       │
    │       ├── services/
    │       │   ├── __init__.py
    │       │   ├── complaint_service.py
    │       │   └── pdf_extractor.py
    │       │
    │       ├── __init__.py
    │       └── main.py
    │
    ├── frontend/
    │   ├── public/
    │   ├── src/
    │   │   ├── app/
    │   │   │   └── store.js
    │   │   │
    │   │   ├── features/
    │   │   │   └── complaint/
    │   │   │       └── complaintSlice.js
    │   │   │
    │   │   ├── services/
    │   │   │   └── complaintApi.js
    │   │   │
    │   │   ├── App.css
    │   │   ├── App.jsx
    │   │   ├── index.css
    │   │   └── main.jsx
    │   │
    │   ├── index.html
    │   ├── package.json
    │   ├── package-lock.json
    │   └── vite.config.js
    │
    ├── .gitignore
    └── README.md

---

## Backend API

The backend is implemented using FastAPI.

### Process Complaint

    POST /api/complaints/process

Processes a natural-language customer complaint using the LangGraph and Groq AI workflow.

---

### Edit Complaint

    POST /api/complaints/edit

Updates an existing complaint using an AI-assisted correction.

The request contains:

- Current complaint
- Edit instruction

The response contains the complete updated complaint and updated risk assessment.

---

### Extract Complaint from PDF

    POST /api/complaints/extract-document

Accepts a pharmaceutical complaint PDF and extracts structured complaint information.

---

### Check Complaint Completeness

    POST /api/complaints/check-completeness

Checks the completeness of the current complaint using the Complaint Completeness Checker.

---

### Health Check

    GET /health

Returns the backend service health status.

---

### Database Health Check

    GET /health/database

Checks whether the backend can successfully connect to PostgreSQL.

---

### API Documentation

FastAPI automatically provides interactive Swagger documentation.

Once the backend is running, open:

    http://127.0.0.1:8000/docs

---

## Database

The application uses PostgreSQL for complaint persistence.

The database used by the project is:

    aivoa_complaints

The complaint model stores information including:

- Customer information
- Product information
- Batch information
- Manufacturing and expiry dates
- Affected quantity
- Complaint description
- Facility information
- Material impact
- Defect information
- Severity
- Risk level
- Recommended action
- Risk rationale
- Complaint source
- Creation and update timestamps

The backend creates the required database table using SQLAlchemy when the application starts.

---

## Redux State Management

The React frontend uses Redux Toolkit to manage complaint state.

The complaint state contains:

- Complaint information
- Risk assessment
- Application status

The Redux complaint slice provides actions for:

- Setting an AI-generated complaint result
- Updating complaint information
- Clearing the current complaint

This allows the AI-generated information returned by the backend to be reflected consistently across the frontend interface.

---

## Environment Variables

The backend uses environment variables for database and Groq configuration.

Create:

    backend/.env

Example structure:

    DATABASE_URL=postgresql+psycopg://<username>:<password>@localhost:5432/aivoa_complaints
    GROQ_API_KEY=<your_groq_api_key>
    GROQ_MODEL=<your_groq_model>

Do not commit the `.env` file to GitHub.

The repository `.gitignore` excludes environment files and local development dependencies.

---

## Installation

### 1. Clone the Repository

    git clone https://github.com/HemanthLove/aivoa-customer-complaint-management.git

### 2. Move into the Project

    cd aivoa-customer-complaint-management

---

## Backend Setup

### 1. Move into the Backend

    cd backend

### 2. Create a Python Virtual Environment

For Python 3.11:

    py -V:Astral/CPython3.11.15 -m venv .venv

### 3. Activate the Virtual Environment

For Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

### 4. Install Dependencies

    pip install "fastapi[standard]" langgraph langchain langchain-groq sqlalchemy "psycopg[binary]" pydantic-settings python-multipart pypdf

### 5. Configure Environment Variables

Create:

    backend/.env

Add the required PostgreSQL and Groq configuration.

### 6. Start the Backend

    uvicorn app.main:app --reload

The backend will be available at:

    http://127.0.0.1:8000

Swagger documentation:

    http://127.0.0.1:8000/docs

---

## Frontend Setup

Open a second terminal.

### 1. Move into the Frontend

    cd frontend

### 2. Install Dependencies

    npm install

### 3. Start the Development Server

    npm run dev

The frontend will normally be available at:

    http://localhost:5173

---

## Running the Application

Start the backend first:

    cd backend
    .\.venv\Scripts\Activate.ps1
    uvicorn app.main:app --reload

Then start the frontend in another terminal:

    cd frontend
    npm run dev

Open the frontend in the browser:

    http://localhost:5173

---

## Example Complaint Workflow

A natural-language complaint can be submitted through the AI Copilot.

Example:

    Apollo Pharmacy reported discolored amoxicillin capsules 500 mg.

The AI processes the complaint and extracts the available information.

A correction can then be provided through the Copilot.

Example:

    Sorry, the batch number is BMX240603 and affected quantity is 50 capsules.

The system updates the requested information while preserving the remaining complaint data.

A pharmaceutical complaint PDF can also be uploaded through the Copilot for document extraction.

---

## Complaint Completeness Example

After a complaint has been processed, the Completeness Checker can be run.

It evaluates:

    Customer Name
    Product Name
    Batch Number
    Defect Type
    Affected Quantity
    Complaint Description

Example result:

    Completeness Score: 100
    Status: Complete

The checker also reports the fields that are present or missing and provides notes explaining the result.

---

## Security

Sensitive configuration is kept outside version control.

The following are excluded from GitHub:

- `.env`
- Python virtual environments
- Python cache files
- Node modules
- Frontend build output
- IDE-specific files
- Operating-system generated files

The Groq API key should only be stored in the local environment configuration.

---

## Assignment Alignment

The implementation follows the demonstrated pharmaceutical Customer Complaint workflow.

Implemented core functionality includes:

- AI-assisted complaint logging
- AI-assisted complaint editing
- PDF complaint extraction
- AI-generated risk assessment
- React frontend
- Redux state management
- FastAPI backend
- LangGraph AI workflows
- Groq LLM integration
- PostgreSQL persistence

The following optional bonus functionality has also been implemented:

- Complaint Completeness Checker

The application is designed around the requirement that the user interacts with the AI Copilot to populate and update the complaint form rather than manually entering the complaint information.

---

## Demo Workflow

The application can be demonstrated using the following sequence:

### 1. AI Complaint Logging

Enter a pharmaceutical complaint through the AI Copilot.

Show that the complaint information is automatically extracted and populated into the form.

### 2. Risk Assessment

Show the AI-generated:

- Severity
- Risk level
- Recommended action
- Rationale

### 3. AI Complaint Editing

Provide a correction through the Copilot.

Show that the requested information changes while the remaining complaint information is preserved.

### 4. PDF Extraction

Upload a realistic pharmaceutical complaint PDF.

Show that the extracted complaint information is automatically populated into the form.

### 5. Completeness Checker

Run the optional Complaint Completeness Checker.

Show:

- Completeness score
- Present fields
- Missing fields
- Notes

### 6. Code Walkthrough

Walk through the implementation from:

    Frontend
        ↓
    API Service
        ↓
    FastAPI Endpoint
        ↓
    LangGraph Workflow
        ↓
    Groq LLM
        ↓
    Structured Pydantic Result
        ↓
    Redux State
        ↓
    Complaint Form / Risk Assessment
        ↓
    PostgreSQL

---

## Limitations

- PDF processing currently relies on text extraction from readable PDFs.
- Scanned-image OCR is not implemented.
- The AI output depends on the information available in the provided complaint.
- The system is a technical implementation and does not replace validated pharmaceutical Quality Management System processes.
- AI-generated risk assessments should be reviewed by appropriate domain personnel before being used for real-world quality decisions.
- The application is intended for demonstration and assessment purposes rather than production pharmaceutical deployment.

---

## Future Improvements

Potential future improvements include:

- Production-grade OCR for scanned complaint documents
- More advanced document parsing
- Complaint Root Cause Recommendation
- Duplicate Complaint Detection
- CAPA Recommendation
- Complaint Summary generation
- AI Risk Classification improvements
- Authentication and authorization
- Audit trails
- Role-based access control
- Database migrations
- Production deployment
- Enhanced pharmaceutical QMS integrations

---

## License

This project was developed as part of a technical assessment.

---

## Author

**Hemanth Love**

GitHub:

    https://github.com/HemanthLove/aivoa-customer-complaint-management