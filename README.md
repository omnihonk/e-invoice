# ⚡ Smart ZUGFeRD E-Invoice Backend Service

This backend is a high-performance, modular, and containerized **FastAPI** service for generating, validating, and managing certified European **EN 16931 / ZUGFeRD / Factur-X compliant hybrid electronic invoices**. It unifies database persistence, Jinja2 template rendering, WeasyPrint PDF layout generation, and strict Schematron validation.

---

## 🏗️ System Architecture & Components

The application is structured into clearly separated architectural components unified inside a high-speed, scalable multi-container environment:

```
                  ┌──────────────────────────────────────────────┐
                  │                 Vite Frontend                │
                  └──────────────────────┬───────────────────────┘
                                         │ REST API
                                         ▼
   ┌─────────────────────────────── Docker network ───────────────────────────────┐
   │                                                                              │
   │   ┌────────────────────────── FastAPI Service ──────────────────────────┐    │
   │   │                                                                     │    │
   │   │  ┌──────────────────┐    ┌──────────────────┐    ┌───────────────┐  │    │
   │   │  │  API Validations │    │ Jinja2 Templates │    │  PDF Service  │  │    │
   │   │  │  (schemas/)      │    │ (fks_invoice)    │    │  (WeasyPrint) │  │    │
   │   │  └────────┬─────────┘    └────────┬─────────┘    └───────┬───────┘  │    │
   │   │           │                       │                      │          │    │
   │   │           ▼                       ▼                      ▼          │    │
   │   │  ┌──────────────────────────────────────────────────────────────┐  │    │
   │   │  │                    services/service.py                       │  │    │
   │   │  └──────────────────────────────┬───────────────────────────────┘  │    │
   │   │                                 │ Shell Exec                       │    │
   │   │                                 ▼                                  │    │
   │   │  ┌──────────────────────────────────────────────────────────────┐  │    │
   │   │  │                     Mustangproject CLI                       │  │    │
   │   │  │  OpenJDK 21 JRE ──► Mustang-CLI-2.23.0.jar (Validation)      │  │    │
   │   │  └──────────────────────────────┬───────────────────────────────┘  │    │
   │   └─────────────────────────────────┼───────────────────────────────────┘    │
   │                                     │                                        │
   │                                     ▼                                        │
   │   ┌─────────────────────────────────────────────────────────────────────┐    │
   │   │                           Redis Container                           │    │
   │   │   Fast, flaccid, transient session drafts (InvoiceSession JSON)     │    │
   │   └─────────────────────────────────────────────────────────────────────┘    │
   └──────────────────────────────────────────────────────────────────────────────┘
                                         │ SQLite volume mount
                                         ▼
                      ┌──────────────────────────────────────┐
                      │             Host Machine             │
                      │  Persistent SQLite: data/e_invoice.db│
                      └──────────────────────────────────────┘
```

### 1. The Core Services
* **PDF Service (`pdf_service.py`)**: Responsible for compiling the structural invoice skeletons via HTML template inheritance (`base_invoice.html` and `fks_invoice.html`), dynamically applying layout styles, logo base64 embeddings, currency filters, and compiling directly to PDF using **WeasyPrint**.
* **DraftHorse & Factur-X Engine (`service.py`)**: Utilizes standard CII namespaces to construct compliant XML documents from invoice sessions and embeds this machine-readable XML structure directly into the generated PDF metadata.
* **Mustang Validation Service (`validation_service.py`)**: Coordinates the automatic verification of generated invoices against official Schematron / XSD standard rules using the packaged `Mustang-CLI` validator.

---

## 💾 Relational SQLite vs. Transient Redis Sessions

To keep the application highly performant and maintain clean boundaries, we enforce a strict separation of concerns:

### 📁 Database Models (`models/` via SQLModel)
* **What**: Represents **persistent Master Data** (Stammdaten) stored on disk inside an SQLite database (`data/e_invoice.db`).
* **Why**: It is designed to act as a reusable registry (Address Book) for business entities—allowing you to store multiple clients (`BuyerTradeParty`), supplier identities (`SellerTradeParty`), and product lists (`Product`) for recurring use.
* **Volume Persistence**: In Docker Compose, the host `./data` directory is mounted at `/app/data` inside the container. This ensures your master data and SQL schemas remain **100% persistent** across container redeployments and restarts.

### ⚡ Session Schemas (`schemas/` via Pydantic)
* **What**: Represents **transient Transaction Data** (flüchtige Session-Entwürfe) compiled dynamically when drafting a new invoice.
* **Why**: When a user begins creating an invoice, they create a draft (`InvoiceSession`). Since this session is temporary, we serialize it to JSON and store it in **Redis** with a TTL cache. Once the invoice is validated and downloaded, the session is cleared. 
* **Benefits**: Decouples relational SQLite tables from high-frequency temporary operations, avoiding database bloat and migration requirements.

---

## ☕ OpenJDK 21 & Mustang-CLI Validation

E-invoices are business-critical documents that require official validation. 

* **The Engine**: We use [Mustangproject](https://github.com/ZUGFeRD/mustangproject)—a Java e-invoicing library designed specifically to read, write, and validate ZUGFeRD / Factur-X formats.
* **Runtime**: The validation service executes `Mustang-CLI-2.23.0.jar` by invoking standard shell processes (`java -jar`). The Docker container comes pre-bundled with **OpenJDK JRE 21** to handle these execution flows seamlessly and offline.
* **Parser**: The `validation_service.py` runs validation compliance checks, extracts detailed statistics (such as standard rules evaluated, failed assertions, and durations), and parses both XML compliance and PDF/A layout compliance structures, making this metadata available directly to the frontend.

---

## 🐳 Docker Services & Compose Architecture

The application is orchestrated via **Docker Compose** across a virtual bridge network:
* **`web` service**: Build layer on `python:3.12-slim` containing WeasyPrint dependencies, OpenJDK JRE 21, the cached Mustang JAR, FastAPI code, and host volume mappings (`./data` mapped to `/app/data`).
* **`redis` service**: A lightweight Alpine Redis companion used for rapid API session token storage.

---

## 🚀 Step-by-Step Deployment Guide

Ensure you have **Docker** and **Docker Compose** installed (or Podman equivalent with compose support).

### 1. Build and Launch Containers
To build the backend image and spin up the services in detached mode:
```bash
docker compose up --build -d
```

### 2. Verify Container Health
Check that both the web server and the Redis database are running and mapping ports:
```bash
docker compose ps
```
The backend will be available at `http://localhost:8000`.

### 3. Run Automated Tests Inside the Container
Verify that all 141 tests (PDF rendering, XML well-formedness, database schemas, and Mustang validation) pass inside the active JRE container environment:
```bash
docker compose exec web pytest -v
```

### 4. Stop Services
To shut down the containers while preserving your persistent database directory:
```bash
docker compose down
```

---

## 📡 REST API Specifications

The FastAPI server exposes clear endpoints for persistent registries, session drafting, and ZUGFeRD generation:

### 🧾 Invoice Session Workflow (`/session`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/session/start` | Creates a new transient invoice drafting session. Returns `session_id` (UUID). |
| **POST** | `/session/{session_id}/seller` | Saves the Seller (Lieferant) profile details to the session cache. |
| **POST** | `/session/{session_id}/buyer` | Saves the Buyer (Kunde) profile details and transaction parameters to the session. |
| **POST** | `/session/{session_id}/items` | Registers the spreadsheet invoice line items (quantities, prices, FKS fields) into the session. |
| **POST** | `/session/{session_id}/generate` | Generates the hybrid e-invoice PDF/A containing the embedded CII XML and returns it as a direct download. |
| **POST** | `/session/{session_id}/validate` | Triggers the in-container Mustang Schematron validation, returning rule execution stats and error lists. |

### 🗃️ Registry Masters (`/sellers`, `/buyers`, `/products`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/sellers/` | Adds a new persistent Seller profile to the SQLite database. |
| **GET** | `/all_sellers` | Retrieves all registered Seller profiles from the database. |
| **GET** | `/sellers/{party_id}` | Retrieves details for a specific registered Seller. |
| **POST** | `/buyers/` | Adds a new persistent Buyer profile to the SQLite database. |
| **GET** | `/all_buyers` | Retrieves all registered Buyer profiles from the database. |
| **POST** | `/products/` | Adds a new persistent Product entry to the catalog. |
| **GET** | `/all_products` | Retrieves all persistent catalog products. |
