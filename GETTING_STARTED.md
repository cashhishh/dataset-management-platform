# 🚀 Getting Started Checklist

Complete this checklist to get your Multi-User Dataset Management Platform running.

---

## ✅ Pre-Flight Checklist

### 1. Prerequisites Installed
- [ ] Python 3.8 or higher (`python --version`)
- [ ] PostgreSQL 12 or higher (`psql --version`)
- [ ] pip package manager (`pip --version`)
- [ ] Git (optional, for version control)

### 2. PostgreSQL Setup
```bash
# Start PostgreSQL service (if not running)
# Windows: Services → PostgreSQL
# Mac: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Create database
psql -U postgres
CREATE DATABASE dataset_platform;
\q
```
- [ ] PostgreSQL service is running
- [ ] Database `dataset_platform` created
- [ ] You know your PostgreSQL password

### 3. Project Configuration
```bash
# Navigate to backend directory
cd backend

# Update database password in app/db.py
# Change line 15:
#   "password": "postgres"  # <- Change this to your password
```
- [ ] Updated PostgreSQL password in `app/db.py`
- [ ] Reviewed `.env.example` (optional)

### 4. Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt
```
- [ ] All packages installed successfully
- [ ] No installation errors

---

## 🏃 Launch Checklist

### 5. Start the Server
```bash
# Make sure you're in the backend directory
cd backend

# Run the application
python app/main.py
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Database connection pool created successfully
INFO:     Database tables created successfully
INFO:     Application started successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

- [ ] Server started without errors
- [ ] Tables auto-created successfully
- [ ] Server running on port 8000

### 6. Verify Server is Running
```bash
# In a new terminal
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status": "healthy", "database": "connected"}
```

- [ ] Health check returns 200 OK
- [ ] Response shows "healthy" status

### 7. View API Documentation
Open in browser:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

- [ ] API docs page loads successfully
- [ ] All endpoints visible (auth, datasets)

---

## 🧪 Testing Checklist

### 8. Run Automated Tests
```bash
# In backend directory
python test_api.py
```

**Expected Output:**
```
[TEST] Health Check
✓ Server is running

[TEST] User Registration
✓ Regular user registered successfully

... (more tests)

Test Summary
===========
Passed: 11
Failed: 0

✓ All tests passed! Your API is working correctly.
```

- [ ] All tests passed
- [ ] No errors in test output
- [ ] Users created successfully
- [ ] Datasets created successfully

### 9. Manual Testing (Optional)
Using the interactive docs at http://localhost:8000/docs:

**Step A: Register a User**
- [ ] Click `POST /auth/register`
- [ ] Click "Try it out"
- [ ] Enter test data
- [ ] Click "Execute"
- [ ] Response: 201 Created

**Step B: Login**
- [ ] Click `POST /auth/login`
- [ ] Enter same email/password
- [ ] Copy the `access_token`

**Step C: Authorize**
- [ ] Click green "Authorize" button (top right)
- [ ] Enter: `Bearer YOUR_TOKEN`
- [ ] Click "Authorize"

**Step D: Create Dataset**
- [ ] Click `POST /datasets/`
- [ ] Enter dataset info
- [ ] Click "Execute"
- [ ] Response: 201 Created

**Step E: View Datasets**
- [ ] Click `GET /datasets/`
- [ ] Click "Execute"
- [ ] Your dataset appears in response

---

## 🎯 Success Criteria

You're ready when:
- [x] Server starts without errors
- [x] Database tables auto-created
- [x] Health check returns 200 OK
- [x] API docs are accessible
- [x] Automated tests pass
- [x] Can register users
- [x] Can login and get JWT token
- [x] Can create datasets
- [x] Can view datasets

**If all checked: Congratulations! 🎉 Your backend is running perfectly.**

---

## ❌ Troubleshooting

### Issue: "could not connect to server"
**Solution:**
1. Check PostgreSQL is running
2. Verify credentials in `app/db.py`
3. Try: `psql -U postgres -c "SELECT version();"`

### Issue: "relation 'users' does not exist"
**Solution:**
1. Restart the server
2. Tables are auto-created on startup
3. Check logs for database connection errors

### Issue: "pip install failed"
**Solution:**
1. Update pip: `pip install --upgrade pip`
2. Install individually: `pip install fastapi uvicorn psycopg2-binary`
3. Check Python version: `python --version` (need 3.8+)

### Issue: "Port 8000 already in use"
**Solution:**
1. Kill existing process on port 8000
2. Or change port in `app/main.py` (line 93)

### Issue: "401 Unauthorized"
**Solution:**
1. Login again to get fresh token
2. Tokens expire after 30 minutes
3. Make sure you clicked "Authorize" button

### Issue: Test script fails
**Solution:**
1. Make sure server is running first
2. Database must be empty or use existing test users
3. Check server logs for errors

---

## 📚 Next Steps

Once everything is working:

### Learning & Exploration
- [ ] Read `ARCHITECTURE.md` to understand design decisions
- [ ] Review `DIAGRAMS.md` for visual architecture
- [ ] Explore code with comments explaining key concepts

### Customization
- [ ] Change JWT secret key in `core/security.py`
- [ ] Adjust token expiration time
- [ ] Modify CORS settings in `main.py`
- [ ] Add custom validation rules

### Enhancement Ideas
- [ ] Add file upload functionality
- [ ] Implement pagination for datasets list
- [ ] Add search/filter capabilities
- [ ] Implement password reset flow
- [ ] Add user profile updates
- [ ] Create dataset sharing between users

### Deployment Preparation
- [ ] Move secrets to environment variables
- [ ] Create Dockerfile
- [ ] Set up CI/CD pipeline
- [ ] Configure production database
- [ ] Set up monitoring/logging

### Resume & Interview Prep
- [ ] Practice explaining architecture
- [ ] Prepare demo walkthrough
- [ ] Review security implementations
- [ ] Understand all design decisions

---

## 📞 Quick Reference

### Start Server
```bash
cd backend
python app/main.py
```

### Run Tests
```bash
cd backend
python test_api.py
```

### Database Access
```bash
psql -U postgres dataset_platform
```

### View Logs
Server logs appear in terminal where you ran `python app/main.py`

### API Docs
http://localhost:8000/docs

### Health Check
http://localhost:8000/health

---

## ✨ You're All Set!

Your production-ready backend is now running. Great job! 🚀

**Next:** Start experimenting with the API, read the documentation, and prepare for interviews!
