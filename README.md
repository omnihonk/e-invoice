# E-Invoice Backend

Web service built with **FastAPI**, **SQLModel**, and **Redis** for generating, managing, and persisting legally compliant electronic invoices under the  **ZUGFeRD / Factur-X** standard.

---

## Features

- **ZUGFeRD 2.2 / Factur-X Compliant**: Generates hybrid PDF invoices containing embedded structured XML invoices (Basic/EN 16931 profile).
- **Dual Caching & Persistence Layers**:
  - **Redis Cache**: Holds transient, hot drafts during session editing.
  - **SQLite Database**: Serves as a persistent relational store for historical orders, invoice records, and finalized binary payloads.
- **Modular Architecture**: Decoupled, service-oriented design splitting routing, database persistence, ZUGFeRD assembly, and PDF rendering.
- **Robust REST API**: Rich endpoints supporting full session draft state management and retroactive downloads of signed PDFs and XML schemas.

---

## KOSIT Validation

The Koordinierungsstelle für IT-Standards (KoSIT) offers a [validator](https://github.com/itplr-kosit/validator). Here is a test with [X-Rechnung Config](https://github.com/itplr-kosit/validator-configuration-xrechnung)

```text
KoSIT Validator version 1.6.0
Loading scenarios from  file:///home/rh/kosit-validator/scenarios.xml
Using repository  file:///home/rh/kosit-validator/

Loaded "Validator Configuration XRechnung 3.0.2" by Coordination Office for IT Standards (KoSIT) from 2026-02-04 
The following scenarios are available:
  * EN16931 XRechnung (UBL Invoice)
  * EN16931 XRechnung Extension (UBL Invoice)
  * EN16931 XRechnung CVD (UBL Invoice)
  * EN16931 XRechnung (UBL CreditNote)
  * EN16931 XRechnung CVD (UBL CreditNote)
  * EN16931 XRechnung (CII)
  * EN16931 XRechnung Extension (CII)
  * EN16931 XRechnung CVD (CII)
  * EN16931 (UBL Invoice)
  * EN16931 (UBL CreditNote)
  * EN16931 (CII)


Processing of 1 objects started
Processing of 1 objects completed in 188ms
Results:
---------------------------------------------------------------------------------------------------------
|File                                                 |Schema |Schematron|Acceptance|Error/Description   |
|/home/rh/kosit-validator/invoice_2ddd1007.xml        |   Y   |    Y     |ACCEPTABLE|                    |
---------------------------------------------------------------------------------------------------------
Acceptable:  1  Rejected:  0


##############################
#   Validation successful!   #
##############################
```

---

## Project Structure

```text
e-invoice/
├── constants.py            # Global application constants
├── database/               # Relational database infrastructure
│   ├── db.py               # Engine configuration, sessions, and dynamic migration hooks
│   └── __init__.py
├── main.py                 # FastAPI application startup & middleware setup
├── models/                 # Relational SQLModel schemas
│   ├── invoice_order.py    # Order metadata, number sequence, and binary storage models
│   ├── party.py            # Legal parties (Buyer/Seller) data models
│   └── __init__.py
├── pyproject.toml          # Build configuration and dependencies (pytest, SQLModel, drafthorse)
├── requirements.txt        # Pinned lock-file of dependencies
├── routers/                # FastAPI controller endpoints
│   ├── order.py            # Historical retrieval, binary downloads (PDF/XML)
│   ├── session.py          # Session draft creation, validation, and generation
│   └── __init__.py
├── schemas/                # Pydantic input/output validation models
│   ├── session.py          # InvoiceSession schemas & JSON serialization models
│   └── __init__.py
├── services/               # Core business logic & formatting helper modules
│   ├── service.py          # Orchestrates PDF render -> XML embed -> Binary build pipeline
│   └── __init__.py
├── templates/              # Jinja2 HTML templates for PDF rendering
│   └── layouts/
│       └── base_invoice.html
└── tests/                  # Highly isolated automated test suite
    ├── conftest.py         # DB overrides and Redis mocks
    ├── test_order_api.py   # Suite for persistent order and numbering APIs
    └── __init__.py
```

---

## Installation & Setup

Choose either **Docker Deployment** (recommended, as it automatically bundles Redis and all system library dependencies) or a **Local Setup**.

### Option A: Docker Deployment (Recommended)

This project includes a ready-to-use Docker configuration with `docker-compose`. This manages caching (Redis), all WeasyPrint system-level libraries, and maps persistent database volumes out-of-the-box.

1. **Build and start all services**:
   ```sh
   docker compose up --build -d
   ```
2. **Access the application**:
   The backend API will be running at `http://localhost:8000`.
3. **Check container status**:
   ```sh
   docker compose ps
   ```
4. **Monitor logs**:
   ```sh
   docker compose logs -f
   ```

### Option B: Local Setup

#### Prerequisites

- **Python**: Version `3.11` or higher.
- **Redis**: A running instance on `localhost:6379` (for session draft caching).
- **System dependencies**: `weasyprint` requires `pango` and `cairo` to render HTML templates to PDF. Make sure they are installed on your OS (e.g., `sudo apt install shared-mime-info libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0` on Ubuntu/Debian).

#### 1. Set up the Python virtual environment

Using **uv** (highly recommended for performance):

```sh
uv venv
source .venv/bin/activate
uv sync
```

Alternatively, using standard **pip**:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 2. Spin up the application

Start the hot-reloading development server:

```sh
fastapi dev main.py
```

Or use **uvicorn** directly:

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## API Reference

The API documentation is available at `/docs`.

### Session Drafts (`/sessions`)

Manage and compile transient invoice drafts cached in Redis:

- `POST /sessions` - Initialize a new invoice session draft.
- `GET /sessions/{session_id}` - Retrieve the current draft state.
- `PUT /sessions/{session_id}` - Update the buyer, seller, line items, and taxes.
- `POST /sessions/{session_id}/generate` - Finalize the draft. This compiles the ZUGFeRD standard XML, renders the Weasyprint PDF, registers the consecutive order number, commits all assets to the persistent database, and returns the hybrid PDF binary.
- `POST /sessions/{session_id}/validate` - Validate the generated Factur-X PDF draft using the built-in **Mustang Validator CLI**. Returns a structured JSON validation report detailing European standards compliance.

### Historical Orders (`/orders`)

Inspect finalized orders and retrieve generated regulatory binaries from SQLite:

- `GET /orders` - Fetch a paginated list of all generated orders and metadata.
- `GET /orders/{order_number}` - Retrieve full metadata details for a specific order.
- `GET /orders/{order_number}/pdf` - Download the finalized, ZUGFeRD-compliant hybrid PDF document.
- `GET /orders/{order_number}/xml` - Download the raw embedded ZUGFeRD invoice XML.

---

## ZUGFeRD/Factur-X Validation (Mustang-CLI)

The Docker service integrates a CLI tool to validate the generated invoices against ZUGFeRD 1, 2 or XRechnung Standards. The Tool is provided by [The Mustang Project](https://www.mustangproject.org/)

### How it works:

- **Automatic Provisioning**: On application startup or validation request, the service automatically downloads the official Mustang-CLI jar from Maven Central if not already present locally.
- **Docker-Bundled**: In Docker environments, the Java Runtime (JRE 21) and the `Mustang-CLI.jar` are pre-packaged during the image build process for zero-dependency execution.
- **Validation Report**: Running a validation returns a structured JSON containing validation results:
  ```json
  {
    "is_valid": true,
    "status": "valid",
    "info": {
      "rules": {
        "fired": 142,
        "failed": 0
      }
    },
    "errors": []
  }
  ```

---

## Testing

The test suite runs with fully isolated, in-memory SQLite instances to guarantee that development database states are not contaminated.

Execute all automated tests via **pytest**:

```sh
pytest
```
