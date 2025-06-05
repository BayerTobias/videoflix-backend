# 🎬 Videoflix Backend

This is the **backend** for [Videoflix](https://github.com/BayerTobias/videoflix-frontend-angular-17) — a Netflix-inspired streaming platform built with Django and Django REST Framework.

It handles video management, user authentication, background processing, and optimized delivery via Redis-based caching.

---

## ⚙️ Tech Stack

- **Framework**: Django 5, Django REST Framework
- **Authentication**: Djoser with token authentication
- **Background Jobs**: Django RQ
- **Video Processing**: FFmpeg
- **Caching**: Redis
- **Database**: PostgreSQL

---

## 🚀 Features

- 🔐 Token-based user authentication
- 📦 Upload and manage video files
- 🧠 Automatic video conversion to 720p and 480p
- 🖼️ Thumbnail generation on upload
- 🧰 Background processing using Redis & RQ
- ⚡ Response caching for public/private videos
- 🗑️ Automatic cleanup on video deletion

---

## 📂 API Overview

### Authentication (via Djoser)

- `POST /auth/token/login/` – Log in and retrieve token
- `GET /auth/users/me/` – Get current user

### Video Management

- `GET /api/videos/?visibility=public` – List all public videos
- `GET /api/videos/?visibility=private` – List your private videos
- `POST /api/videos/` – Upload a new video (authenticated)
- `DELETE /api/videos/<id>/` – Delete a video (authenticated)

---

## 🔁 Signal-Based Processing

- On upload:

  - A thumbnail is generated via FFmpeg
  - 720p and 480p conversions are enqueued
  - Cache is cleared

- On deletion:
  - Original, thumbnail, 720p, and 480p files are removed
  - Cache is cleared

---

## 🧪 Local Development Setup

### 1. Environment Variables

Create a `.env` file in your root directory:

```env
SECRET_KEY=your_secret_key
POSTGRESQL_PASSWORD=your_pg_password
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=user@example.com
EMAIL_HOST_PASSWORD=your_email_password
```

### 2. Install & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## 🎥 Frontend

The Angular frontend can be found [here](https://github.com/BayerTobias/videoflix-frontend-angular-17):
