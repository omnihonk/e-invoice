from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from dependencies import get_session
from models.product import Product
from typing import List

router = APIRouter(tags=["products"])

@router.post("/products/", response_model=Product)
def create_product(
    *, session: Session = Depends(get_session), product: Product
):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.get("/products/", response_model=List[Product])
def read_products(*, session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

@router.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, *, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, *, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {"message": f"Product {product_id} deleted successfully"}

@router.post("/invoice-items/")
def create_invoice_items(items: list[dict]):
    print(items)
    return {"message": "Invoice items created", "items": items}
