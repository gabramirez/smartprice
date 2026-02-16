from app.domain.models import PriceSuggestion

def calculate_suggested_price(cost_price: float, market_prices: list[float]) -> float:
    market_avg = sum(market_prices) / len(market_prices)
    candidate_price = market_avg * 0.9
    minimum_allowed = cost_price * 1.05
    return max(candidate_price, minimum_allowed)


def build_price_suggestion(product, market_prices):
    suggested_price = calculate_suggested_price(product.cost_price, market_prices)
    return PriceSuggestion(
        product_id=product.id,
        suggested_price=suggested_price,
        status="Pendente"
    )
