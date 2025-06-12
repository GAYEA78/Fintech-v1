# Arona Fintech Bank

A modern, glassy-UI digital banking app built with Django. Features:

- **User Authentication** with Email-based Two-Factor Authentication (2FA)  
- **Role-based Access** (Admin vs Customer)  
- **Account Management**: deposit funds via Stripe, view balance & transactions  
- **PDF Statements** (downloadable bank statements)  
- **KYC/AML Workflow**: upload & admin approval of identity documents  
- **Responsive, Glass-Blur UI** using CSS custom properties and modern effects  
- **Automated Testing** for core flows (signup, login, deposit)

---

##  Tech Stack

- **Backend:** Python 3.10, Django 4.2  
- **DB:** SQLite (dev), easily switchable to Postgres  
- **Payments:** Stripe Checkout  
- **Email (2FA):** Django console or SMTP (configurable via `.env`)  
- **Frontend:** Bootstrap, CSS  
- **KYC Storage:** Local `media/kyc/` (mock file uploads)

---

## ⚙ Prerequisites

- Python 3.10+ & pip  
- Virtualenv (`python -m venv venv`)  
- [Stripe API keys](https://dashboard.stripe.com/)  
- (Optional) SMTP credentials for real email  
- Git & GitHub account

---

## 🚀 Setup, Run & Deploy

```powershell
# 1. Clone & enter (once your GitHub repo exists)
git clone https://github.com/<YOUR_GITHUB_USERNAME>/banking_app.git
cd banking_app

# 2. Create venv & install
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure env
copy .env.example .env
# Edit .env: add SECRET_KEY, STRIPE_* keys, EMAIL_* settings, etc.

# 4. Database & static
python manage.py migrate
python manage.py collectstatic --noinput

# 5. Create superuser
python manage.py createsuperuser

# 6. Run development server
python manage.py runserver
