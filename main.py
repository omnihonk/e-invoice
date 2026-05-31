import os

from drafthorse.models.document import Document
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import create_db_and_tables
from routers import session as session_router
from routers import seller as seller_router
from routers import buyer as buyer_router
from routers import product as product_router
from routers import order as order_router


def parse_e_invoice_xml():
    sample_xml_path = os.path.join(
        r"C:\Users\heimb\Code\Python\e-invoice\python-drafthorse\tests\samples\zugferd_2p1_EN16931_Einfach.xml"
    )
    sample_xml = open(sample_xml_path, "rb").read()
    doc = Document.parse(sample_xml)

    print(doc)


allowed_origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:4173",  # Vite preview server
]
frontend_port = os.getenv("FRONTEND_PORT")
if frontend_port:
    allowed_origins.append(f"http://localhost:{frontend_port}")
frontend_preview_port = os.getenv("FRONTEND_PREVIEW_PORT")
if frontend_preview_port:
    allowed_origins.append(f"http://localhost:{frontend_preview_port}")

env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    allowed_origins.extend([origin.strip() for origin in env_origins.split(",") if origin.strip()])

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_db_and_tables()

# Include routers
app.include_router(session_router.router)
app.include_router(seller_router.router)
app.include_router(buyer_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)


@app.get("/")
def read_root():
    return {"API": "e-invoice", "docs": "To get started, go to /docs"}


if __name__ == "__main__":
    import uvicorn
    # Use PORT or BACKEND_PORT with fallback to 8000
    port_str = os.getenv("PORT") or os.getenv("BACKEND_PORT") or "8000"
    try:
        port = int(port_str)
    except ValueError:
        port = 8000
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=True)

