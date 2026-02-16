from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.infrastructure.database import SessionLocal
from app.domain.models import Product, CompetitorPrice, PriceSuggestion
from app.application.pricing_service import build_price_suggestion

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/prices/ingest")
def ingest_prices(payload: list[dict], db: Session = Depends(get_db)):

    products_map = {}

    for item in payload:
        product = db.query(Product).filter_by(sku=item["sku"]).first()
        if not product:
            continue

        products_map[item["sku"]] = product

        db.add(
            CompetitorPrice(
                product_id=product.id,
                competitor=item["competitor"],
                price=item["price"]
            )
        )

    db.commit()

    for product in products_map.values():

        prices = db.query(CompetitorPrice.price)\
            .filter_by(product_id=product.id)\
            .all()

        market_prices = [p[0] for p in prices]

        if not market_prices:
            continue

        db.execute(
            delete(PriceSuggestion)
            .where(
                PriceSuggestion.product_id == product.id,
                PriceSuggestion.status == "Pendente"
            )
        )

        suggestion = build_price_suggestion(product, market_prices)

        db.add(suggestion)

    db.commit()

    return {"status": "processed"}


@router.get("/suggestions/pending")
def get_pending(db: Session = Depends(get_db)):

    suggestions = (
        db.query(PriceSuggestion, Product)
        .join(Product, Product.id == PriceSuggestion.product_id)
        .filter(PriceSuggestion.status == "Pendente")
        .all()
    )

    result = []

    for suggestion, product in suggestions:
        result.append({
            "id": suggestion.id,
            "product_id": product.id,
            "product_name": product.name,
            "current_price": product.current_sales_price,
            "suggested_price": suggestion.suggested_price,
            "status": suggestion.status
        })

    return result


@router.post("/suggestions/{suggestion_id}/approve")
def approve(suggestion_id: int, db: Session = Depends(get_db)):

    suggestion = db.query(PriceSuggestion).get(suggestion_id)
    if not suggestion:
        return {"error": "Suggestion not found"}

    product = db.query(Product).get(suggestion.product_id)
    if not product:
        return {"error": "Product not found"}

    product.current_sales_price = suggestion.suggested_price
    suggestion.status = "Aprovado"

    db.commit()

    return {"status": "approved"}
