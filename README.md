# LOGI-TRACK: Fleet Management & Logistics Platform (Version 1)

LOGI-TRACK is a beginner-friendly Fleet Management and Logistics Platform built using fundamental web technologies.
LIVE LINK :https://logi-track-dlw6.onrender.com
## Technology Stack

**Frontend**
- HTML5
- CSS3
- Vanilla JavaScript

**Backend**
- FastAPI (Python)

**Database**
- SQLite

**Maps**
- MapLibre GL JS & OpenStreetMap

**Authentication**
- Simple Company Login (Email + Password)
- Company-ID based authentication
- No JWT
- No Password Hashing
- No OAuth
- No Email Verification

---

# Google Colab Development Workflow

This project is designed to be developed and tested entirely inside **Google Colab**.

Since FastAPI runs inside Google's cloud environment, your browser cannot directly access the server.

To solve this, **Ngrok** is used only as a temporary development tunnel that exposes the FastAPI server to your browser.

**Ngrok is NOT part of the project architecture.**

It is only used during development and testing.

---

# Step 1 - Upload the Project

Upload the complete **LOGI-TRACK** project folder (or a ZIP file containing it) into Google Colab.

If you uploaded a ZIP file, extract it before continuing.

---

# Step 2 - Install Project Dependencies

Install the project dependencies.

```bash
!pip install -r logi-track/requirements.txt
```

> Adjust the folder path if your project is extracted somewhere else.

---

# Step 3 - Install Google Colab Dependencies

Install the additional packages required only for running FastAPI inside Google Colab.

```bash
!pip install pyngrok nest-asyncio
```

These packages are **only required for Google Colab** and are not part of the project itself.

---

# Step 4 - Create a Free Ngrok Account

Create a free account at:

https://ngrok.com/

Copy your **Ngrok Auth Token** from your dashboard.

---

# Step 5 - Configure Ngrok

Open the provided Python script.

Locate the following line:

```python
ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")
```

Replace:

```python
YOUR_NGROK_AUTH_TOKEN
```

with your own Auth Token.

Do not hardcode any personal token into the project before sharing it.

---

# Step 6 - Start the Server

Run the provided FastAPI startup script.

The script will:

- Start the FastAPI server
- Create a temporary Ngrok tunnel
- Display a public URL

Example:

```
https://abcd123.ngrok-free.app
```

---

# Step 7 - Open the Application

Open the generated URL in your browser.

You can now:

- Register a Company
- Login
- Access the Dashboard
- Manage Vehicles
- Test the application

exactly as if it were running on your local machine.

---

# Current Version 1 Features

✔ Company Registration

✔ Company Login

✔ Dashboard

✔ Company Settings

✔ Vehicle Management

✔ Vehicle Details

✔ Animated Dashboard

✔ Chart.js Integration

✔ Beautiful Vehicle Cards

✔ Responsive Layout

✔ Glassmorphism UI

✔ MapLibre + OpenStreetMap Ready

---

# Notes

- Google Colab is the primary development environment for this project.
- No virtual environment (venv) is required.
- No JWT or Password Hashing is implemented in Version 1.
- Ngrok is only used for development and testing.
- Future versions may introduce advanced authentication, AI modules, predictive analytics, and real-time GPS integration.
