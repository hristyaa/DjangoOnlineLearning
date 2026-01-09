import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product_name):
    """Создает продукт в страйпе"""
    return stripe.Product.create(name=product_name)


def create_stripe_price(product_id, price):
    """Создает цену в страйпе"""
    return stripe.Price.create(
        product=product_id,
        currency="rub",
        unit_amount=price * 100,
    )


def create_srtipe_session(price):
    """Создает сессию на оплату в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
