# E-Store (Django)

A modern Django-based e-commerce starter project with product browsing, customer profiles, checkout flow, and order history.

## Features

- Product catalog with category filters
- Product detail pages
- Home page with rotating featured-product carousel
- Customer authentication (login/logout)
- Customer profile management (address and personal info)
- Checkout flow with payment method selection
- Persistent order history per customer
- Django admin support for products, categories, orders, and profiles

## Tech Stack

- Python 3
- Django 6
- SQLite (default)
- HTML + CSS + vanilla JavaScript

## Project Structure

```text
e-store/
  config/                  # Django project settings and URLs
  store/                   # Main app (models, views, templates, URLs)
  static/store/styles.css  # Global styles
  templates/registration/  # Auth templates (login)
  manage.py
  requirements.txt
```

## Quick Start

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Run migrations
5. Start the server

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## Create Admin User

```bash
python manage.py createsuperuser
```

Then open:

- `http://127.0.0.1:8000/admin/`

## Key Routes

- `/` - Home
- `/catalog/` - Product catalog
- `/product/<slug>/` - Product details
- `/checkout/<slug>/` - Checkout (login required)
- `/payment/success/<order_id>/` - Payment success (login required)
- `/orders/` - My Orders (login required)
- `/profile/` - My Profile (login required)
- `/accounts/login/` - Login
- `/admin/` - Django Admin

## Notes

- Sample products are auto-seeded from app logic if not present.
- Current payment flow is simulated (no external gateway integration yet).

## Future Improvements

- Integrate real payment gateways (Razorpay/Stripe)
- Add cart and multi-item checkout
- Add search, sorting, and pagination
- Add automated tests and CI
