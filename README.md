# TMF Marketplace Backend 🚀

The backend API for the **TMF Marketplace**, a premium digital asset platform. Built with **Django Rest Framework (DRF)**.

## 🛠 Tech Stack

-   **Framework**: Django 6.0, Django Rest Framework
-   **Database**: PostgreSQL (Production), SQLite (Dev)
-   **Authentication**: JWT (SimpleJWT)
-   **Storage**: AWS S3 (Media), WhiteNoise (Static)
-   **Deployment**: Docker, Render.com

## ⚡️ Quick Start

### Prerequisites
-   Python 3.10+
-   PostgreSQL (Optional, defaults to SQLite locally)

### 1. Clone & Install
```bash
git clone <your-backend-repo-url>
cd tmf_marketplace_backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the root:
```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=*
DATABASE_URL=postgres://user:pass@localhost:5432/db_name  # Optional
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
```

### 3. Run Locally
```bash
# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```
API will be available at `http://localhost:8000/api/`.

## 🐳 Docker Support
A `Dockerfile` is included for containerized deployment.
```bash
docker build -t tmf-backend .
docker run -p 8000:8000 tmf-backend
```

## 🚀 Deployment (Render.com)
This repo includes `render.yaml` for zero-config deployment on Render.
1.  Connect this repo to Render.
2.  Select "Web Service".
3.  Add environment variables used in `.env`.

## 📚 API Documentation
-   **Auth**: `/api/auth/login/`, `/api/auth/register/`
-   **Photos**: `/api/photos/` (List), `/api/photos/upload/` (Multipart)
-   **Users**: `/api/users/profile/`

**Note**: This project is configured to use AWS S3 for media storage. Ensure AWS credentials are set for image uploads to work.
