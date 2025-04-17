
# 🌐 TradeConnect

**TradeConnect** is a full-stack web platform built with Flask, SQLAlchemy and Bootstrap that connects clients with professionals for service scheduling. It includes role-based dashboards (Admin, Professional, Client), live notifications, Google Maps integration, and service reviews.

> ✅ Live demo: [https://tradeconnect-viem.onrender.com](https://tradeconnect-viem.onrender.com)

---

## 🚀 Features

- 👥 User Roles: Admin, Client, Professional  
- 📆 Schedule Services: Clients can create services with date, time, address (with location autocomplete)  
- 🗺️ Maps Integration: Professionals and clients see services/professionals on a live map  
- 🔔 Notifications: Professionals get notified about new scheduled services  
- 📩 Service Status: Accept or reject services  
- ⭐ Review System: Clients can review professionals  
- 🧭 Google Maps API: Address autocomplete + location markers  
- 🔐 Login/Auth: Session management with Flask-Login  
- 🧾 Admin Panel: Activate/deactivate users and view logs  
- 🌍 Landing Page: Custom responsive landing page  
- ☁️ Cloud Deployment: Hosted on [Render](https://render.com)

---

## 🛠️ Tech Stack

- Backend: Python, Flask, SQLAlchemy, Flask-Login  
- Frontend: HTML, Jinja2, Bootstrap 5, JavaScript  
- Database (local/deploy): SQLite  
- Maps API: Google Maps JavaScript + Places Autocomplete  
- Hosting: Render  
- Version Control: Git + GitHub  

---

## 🧪 Local Development Setup

### 📦 Prerequisites

Ensure the following are installed:

- ✅ [Python 3.10+](https://www.python.org/downloads/)
- ✅ [Git](https://git-scm.com/)
- (Optional) [VS Code](https://code.visualstudio.com/) for editing

---

### 🚀 How to Run the Project Locally

#### 1. Clone the repository

```bash
git clone https://github.com/seuusuario/seurepositorio.git
cd seurepositorio
```

#### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

- On Windows:
```bash
venv\Scripts\activate
```

- On Mac/Linux:
```bash
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run the app for the first time

```bash
python main.py
```

Then, visit this URL in your browser to set up the database and add sample users:

```
http://localhost:5000/setup-forcado
```

---

### 👤 Test Accounts

| Role         | Email                    | Password           |
|--------------|--------------------------|---------------------|
| Admin        | admin@tradeconnect.com   | UltraSecurePass123 |
| Client       | cliente@tradeconnect.com | Cliente123         |
| Professional | pro@tradeconnect.com     | Pro123             |

---

### 🔁 Normal Usage (after setup)

To run the system again, use:

```bash
python main.py
```

Visit:
```
http://localhost:5000
```

---

## 🌐 Google Maps Integration

- This app uses Google Maps API for location autocomplete.
- To use your own key, edit the following line in `schedule_service.html`:

```html
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY_HERE&libraries=places&callback=initAutocomplete" async defer></script>
```

---

## 📁 Project Structure (simplified)

```
/app
  /templates
  /static
  models.py
  routes.py
main.py
requirements.txt
Procfile (for deploy)
README.md
```

---

## ☁️ Deployment

- Ready to deploy on [Render](https://render.com)
- Live site: [https://tradeconnect-viem.onrender.com](https://tradeconnect-viem.onrender.com)

---

## 📧 Contact

Made by [Cleiton](https://github.com/CleitoSilva))
