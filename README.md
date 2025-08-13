```markdown
# 📚 Bookstore / Restful Booker API Automation (Pytest + Requests)

A **complete API automation testing** framework using **Python, Pytest, Requests, and JSON Schema** with **HTML** and **Allure** reporting.

**Target API:** [Restful Booker](https://restful-booker.herokuapp.com/) (public demo API).  

---

## 🔑 API Authentication

**Login Endpoint:**
```

POST /auth

````
**Request Body:**
```json
{
  "username": "admin",
  "password": "password123"
}
````

**Response:**

```json
{ "token": "..." }
```

For **PUT / PATCH / DELETE** requests:
Add header:

```
Cookie: token=<token>
```

> 💡 If the demo API is down in your region, update the `base_url` in `config/config.json` to use a local mock server or another compatible API.

---

## 📂 Project Structure

```
api_automation/
  tests/
    test_create_booking.py
    test_get_booking.py
    test_update_booking.py
    test_delete_booking.py
  utils/
    api_client.py
    schema_validator.py
  config/
    config.json
    test_data.json
  reports/
  requirements.txt
  run_tests.py
  README.md
```

---

## ⚡ Quick Start

### 1️⃣ Create a Virtual Environment

```bash
python -m venv .venv
# Activate (Windows)
.\.venv\Scripts\activate
# Activate (macOS/Linux)
source .venv/bin/activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Tests (Recommended Way)

```bash
# Simple run
python run_tests.py

# Verbose output
python run_tests.py -v

# With HTML report
python run_tests.py --html

# With Allure report
python run_tests.py --allure
```

### 4️⃣ Alternative: Run with Pytest

```bash
# Basic run
pytest tests/

# HTML report
pytest -v --html=reports/report.html --self-contained-html

# Allure report
pytest -v --alluredir=reports/allure-results
# Then (if allure CLI is installed):
allure serve reports/allure-results
```

---

## ⚙ Environment Config

Edit `config/config.json`:

```json
{
  "base_url": "https://restful-booker.herokuapp.com",
  "username": "admin",
  "password": "password123",
  "timeout_seconds": 10
}
```

---

## 📊 Test Data

All payloads are stored in:

```
config/test_data.json
```

You can add new datasets without changing the test code — the framework loads them dynamically.

---

## 🧹 Features

✅ Create, Get, Update, and Delete bookings
✅ Automatic auth token retrieval for update/delete requests
✅ JSON Schema validation for API responses
✅ Data-driven testing using external JSON
✅ Cross-platform compatibility
✅ Supports HTML & Allure reports
✅ Robust error handling with clear assertion messages

---

## 📝 Notes

* Each test creates its own booking and cleans up afterward (where applicable).
* The Restful Booker demo API can be unstable — if you face downtime, switch `base_url` to a local mock.
* Works on **Windows, macOS, and Linux**.

---

## 📌 Example Command for Full Test with Report

```bash
pytest -v --html=reports/report.html --self-contained-html
```

---

## 🔗 References

* [Restful Booker API Docs](https://restful-booker.herokuapp.com/apidoc/index.html)
* [Pytest Documentation](https://docs.pytest.org/en/stable/)
* [Allure Reports](https://docs.qameta.io/allure/)

```

---

