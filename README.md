# Arona Fintech – Secure Banking & Investment Simulation


Fully developped Application Website: https://secure-fund.onrender.com/ 



## A modern full stack fintech web app that combines secure banking, smart investing, KYC onboarding, and a full ledger system. Designed to replicate the features of a digital bank and robo-advisor.

Features Overview
Secure login with 2FA (email-based OTP)

 KYC (Know Your Customer) & Compliance
- Secure document upload system
- Admin-side approval/rejection workflow
- Document versioning & status tracking

User profiling with automatic portfolio recommendation

Manual and automatic rebalancing tools

Stripe-powered deposit system with confirmation flow

Complete transaction history with downloadable PDF statements

Simulated trading system with portfolio tracking

Real-time stock data from Yahoo Finance

Role-based admin dashboard with account/user/KYC control

Chat system between users and administrators

---

## Why does this project matter?

### 1. Traditional Banking Limitations
- Problem: Outdated interfaces and disconnected financial data.
- My Solution: Responsive UI with modern dashboard and real-time stock insights.

### 2. Security & Compliance Gaps
- Problem: Weak authentication and no identity verification.
- My Solution: Email-based 2FA,  document review, and admin role separation.

### 3. Lack of Financial Intelligence
- Problem: No personalized investment options or risk analysis.
- My Solution: Investor profiling, auto-matched portfolios, and drift alerts.

### 4. Transaction Inaccuracies
- Problem: Poor balance tracking and missing audit trails.
- My Solution: Double-entry ledger system with full transaction history.

### 5. Disconnected Customer Support
- Problem: No internal messaging or conversation tracking.
- My Solution: Built-in chat between users and admins with history tracking.

### 6. Payment Integration Challenges
- Problem: Insecure or manual payment handling.
- My Solution: Stripe Checkout with proper redirection and confirmation views.

### 7. Missing Financial Education Tools
- Problem: Users can't learn investing through the app.
- My Solution: Simulated trading, asset visualization, and portfolio tracking.

### 8. Operational Inefficiencies for Admins
- Problem: No centralized admin control.
- My Solution: Admin dashboard with account control, user messaging, and  tools.

---

## APIs and External Services Used

| Purpose                          | Tool / API             | Description                                          |
|----------------------------------|-------------------------|------------------------------------------------------|
| Stock Prices                     | yfinance                | Real-time and historical data from Yahoo Finance     |
| Payments                         | Stripe Checkout         | PCI-compliant card payments                          |
| 2FA via Email                    | Django Email + SMTP     | Sends one-time login codes via email                 |
| PDF Statements                   | ReportLab               | Generates PDF of user transaction history            |
| Data Visualizations              | Chart.js                | Asset and price trend charts                         |

---

## How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/GAYEA78/Secure-Fund.git
cd Secure-Fund
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

### 6. Run the Server
```bash
python manage.py runserver
```

