import os

from drafthorse.models.document import Document
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import create_db_and_tables
from routers import session as session_router
from routers import seller as seller_router
from routers import buyer as buyer_router
from routers import product as product_router


def parse_e_invoice_xml():
    sample_xml_path = os.path.join(
        r"C:\Users\heimb\Code\Python\e-invoice\python-drafthorse\tests\samples\zugferd_2p1_EN16931_Einfach.xml"
    )
    sample_xml = open(sample_xml_path, "rb").read()
    doc = Document.parse(sample_xml)

    print(doc)


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
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


@app.get("/")
def read_root():
    return {"Hello": "World"}
