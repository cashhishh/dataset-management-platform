# 📊 Dataset Management & Quality Analysis Platform

A full-stack web application that allows users to securely upload CSV datasets,
analyze data quality, and manage datasets with persistent authentication.

Built with **FastAPI (backend)** and **React (frontend)**, featuring **JWT-based auth**,
session persistence, and a modern responsive UI.

---

## 🚀 Features

### 🔐 Authentication
- JWT authentication
- Persistent login across refresh & tab reopen
- Protected routes
- Role-based access (user / admin)
- Account history on login (email only, no passwords stored)
- Secure logout & session handling

### 📁 Dataset Management
- Upload CSV datasets
- Automatic metadata extraction:
  - File name & size
  - Row count
  - Column count
- Dataset listing & deletion
- Dataset preview (first N rows)

### 📈 Data Quality Analysis
- Null values per column
- Duplicate row detection
- Completeness score (%)
- Column schema detection (name, type, index)

### 🎨 Frontend UX
- Fully responsive (mobile / tablet / desktop)
- Clean dashboard UI
- Defensive rendering & error handling
- Smooth loading states
- Professional auth flow

---

## 🛠 Tech Stack

### Backend
- FastAPI
- SQLite
- JWT Authentication
- Pandas (CSV parsing & analysis)

### Frontend
- React (Vite)
- React Router
- Axios
- Tailwind CSS

---

