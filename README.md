# Dress E-Commerce Platform

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![Django Version](https://img.shields.io/badge/django-4.x-lightgrey.svg)

A polished, production-ready Django application built as a demonstration of a full-stack e-commerce experience, tailored for dresses but easily adaptable to other product types. This project can be used as a portfolio piece, showcasing backend API design, frontend user flows, third-party integration, and deployment practices.

---

## 🔍 Overview

The system supports:

- **Dynamic product catalog** with categories and filters.
- **Persistent shopping cart** with quantity adjustments.
- **Multi-step checkout** including shipping address, order review, and payment.
- **Payment gateway integration** using Razorpay (configurable for others).
- **User management**: registration, login, password recovery, email/phone verification.
- **Order tracking** and history for customers.
- **Admin panel** for content management and order processing.

This repository is intentionally modular; each Django app encapsulates a specific domain (core, cart, payment), enabling reuse or extraction in other projects.

---

## ⚙️ Technologies & Dependencies

- **Backend**: Python 3.11+, Django 4.x
- **Database**: SQLite (development), PostgreSQL/MySQL recommended for production
- **Payment**: Razorpay (with adapters for other services possible)
- **Frontend**: HTML5, CSS3, vanilla JavaScript, Django template language
- **Testing**: Django’s built-in test framework
- **Deployment**: Gunicorn/uWSGI, Nginx, Heroku/Render/any WSGI host


---

## 📁 Repository Structure

```
├── cart/               # Cart app (models, views, context processor)
├── core/               # Core functionality (products, categories)
├── payment/            # Order and payment processing
├── templates/          # Page templates (organized by feature)
├── static/             # Stylesheets, scripts, images
├── media/              # Uploaded files (product images)
├── manage.py           # Django management utility
├── requirements.txt    # Exact Python dependencies
├── pyproject.toml      # Project metadata (optional)
├── db.sqlite3          # Development database (ignored in git)
└── README.md           # <-- you're reading it
```

Each app contains its own `tests.py` to verify behavior, encouraging test-driven development and code reliability.

---

## ✅ Getting Started (Developer Setup)

1. **Fork & Clone**
   ```bash
   git clone https://github.com/<your-username>/dress_ecommerce.git
   cd e_commerce_site
   ```
2. **Environment**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # Windows PowerShell
   pip install -r requirements.txt
   ```
3. **Configuration**
   - Copy `e_commerce_site/settings_example.py` to `e_commerce_site/settings.py` and adjust.
   - Set environment variables:
     ```powershell
     $env:DJANGO_SECRET_KEY="your-secret-key"
     $env:RAZORPAY_KEY_ID="your-key-id"
     $env:RAZORPAY_KEY_SECRET="your-key-secret"
     ```
   - For production, configure `DATABASE_URL` and other secrets.
4. **Database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. **Run Locally**
   ```bash
   python manage.py runserver
   ```
   Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to explore the site.


---

## 🧪 Testing & Quality

Automated tests ensure stability and regressions are caught early.

```bash
python manage.py test
```

Tests cover models, views, and form logic. Additional linters (flake8, black) can be run if desired.

---

## 📦 Deployment Guidelines

1. **Select a host** (Heroku, Render, DigitalOcean, etc.).
2. **Use a production database** (PostgreSQL recommended).
3. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```
4. **Configure WSGI** via Gunicorn:
   ```bash
   gunicorn e_commerce_site.wsgi:application
   ```
5. **Set environment variables** securely (SECRET_KEY, DEBUG=False, payment keys).
6. **Serve static/media** with Nginx or your hosting provider’s mechanisms.

## 🤝 Contributing

Contributions are very welcome! To contribute:

1. Fork the repo and create a new branch (`feature/your-feature`).
2. Write tests for your changes.
3. Open a pull request with a clear description.

Please adhere to the existing code style and add documentation where applicable.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact & Portfolio

- **Author**: Maheswara (`@dctn`)
- **Email**: h.maheswara30@gmail.com

Feel free to mention this project in your portfolio as a complete, end-to-end e-commerce application built with Django.

---

> _Build something people want and show it off!_ 🎉

