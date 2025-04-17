# 🌐 TradeConnect

**TradeConnect** is a full-stack web platform built with Flask, SQLAlchemy and Bootstrap that connects clients with professionals for service scheduling. It includes role-based dashboards (Admin, Professional, Client), live notifications, Google Maps integration, and service reviews.

> ✅ Live demo: [https://tradeconnect-viem.onrender.com](https://tradeconnect-viem.onrender.com)

---

## 🚀 Features

- 👥 **User Roles**: Admin, Client, Professional  
- 📆 **Schedule Services**: Clients can create services with date, time, address (with location autocomplete)  
- 🗺️ **Maps Integration**: Professionals and clients see services/professionals on a live map  
- 🔔 **Notifications**: Professionals get notified about new scheduled services  
- 📩 **Service Status**: Accept or reject services  
- ⭐ **Review System**: Clients can review professionals  
- 🧭 **Google Maps API**: Address autocomplete + location markers  
- 🔐 **Login/Auth**: Session management with Flask-Login  
- 🧾 **Admin Panel**: Activate/deactivate users and view logs  
- 🌍 **Landing Page**: Custom responsive landing page  
- ☁️ **Cloud Deployment**: Hosted on [Render](https://render.com)

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML, Jinja2, Bootstrap 5, JavaScript
- **Database (local)**: SQL Server via pyodbc  
- **Database (deploy)**: SQLite for compatibility  
- **Maps API**: Google Maps JavaScript + Places Autocomplete  
- **Hosting**:  https://tradeconnect-viem.onrender.com
- **Version Control**: Git + GitHub  

---

## 🧪 Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/seuusuario/seurepositorio.git
cd seurepositorio
