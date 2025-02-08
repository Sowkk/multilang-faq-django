# Multilingual FAQ Management System

A Django-based REST API for managing Frequently Asked Questions (FAQs) with automatic multi-language translation support. The system provides a robust backend for creating, managing, and retrieving FAQs in multiple languages with built-in caching for optimal performance.

## Features

- 🌐 Automatic translation to multiple languages using Google Translate API
- 📝 WYSIWYG editor support for rich text answers
- 🚀 Redis-based caching for improved performance
- 🔍 Comprehensive API endpoints for FAQ management
- 🎯 Language-specific content retrieval
- 👨‍💼 User-friendly Django admin interface

## Tech Stack

- Django 5.0.2
- Django REST Framework
- django-ckeditor
- Redis (for caching)
- PostgreSQL
- Google Translate API

## Supported Languages

- English (en)
- Hindi (hi)
- Bengali (bn)
- Telugu (te)
- Tamil (ta)
- Malayalam (ml)
- Urdu (ur)
- Korean (ko)
- Traditional Chinese (zh-TW)

## Project Structure

```
BHARATFD/
├── venv/
├── AskMe/
│   ├── AskMe/
│   │   └── settings.py
│   │   └── urls.py
│   ├── faqs/
│   │   ├── static/
│   │   │   └── admin/
│   │   │       └── css/
│   │   │           └── custom_filters.css
│   │   |── migrations/
│   │   ├── views.py/
│   │   ├── models.py
│   │   └── admin.py
│   │   └── tests.py
│   │   └── apps.py
│   │   └── urls.py
│   │   └── serializers.py
│   └── manage.py
│   └── confgtest.py
│   └── pytest.ini
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup Database (PostgreSQL)<br>
Install PostgreSQL<br>
In psql
  ```sql
  psql -U postgres
  CREATE DATABASE <your-db>;
  CREATE USER <your-db-user> WITH PASSWORD <your-user-password>;
  GRANT ALL PRIVILEGES ON DATABASE <your-db> TO <your-db-user>; #db-level permissions
  ALTER USER <your-db-user> CREATEDB;
  ALTER USER <your-db-user> WITH LOGIN;
  GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <your-db-user>;
  ALTER DATABASE <your-db> OWNER TO <your-db-user>;
  GRANT ALL ON SCHEMA public TO djangouser; #schema-level permissions
  ```
6. Configure environment variables (.env):
```env
DEBUG=True
SECRET_KEY=<your-secret-key>
DATABASE_NAME=<your-db>
DATABASE_USER=<your-db-user>
DATABASE_PASSWORD=<your-user-password>
DATABASE_HOST=<localhost>
DATABASE_PORT=<5432>
REDIS_URL=<redis://localhost:6379/1>
```

7. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

8. Create superuser:
```bash
python manage.py createsuperuser
```

9.  Run the redis server:
```bash
redis-server
redis-cli
ping
>pong #running correctly
```
10.  Run the development server:
```bash
python manage.py runserver
```

# API Endpoints

### **List of all FAQs**

**Endpoint:** `GET /api/faqs/`
### **List of FAQs of a language**

**Endpoint:** `GET /api/faqs/?lang=hi  # For Hindi`

### **Create FAQ**

**Endpoint:** `POST /api/faqs/`<br> 
**Response:**
  ```
  {
      "question": "What is...?",
      "answer": "This is..."
  }
  ```
### **Update FAQ**

**Endpoint:** `PUT /api/faqs/{id}/`<br> 
**Response:**
  ```{
    "question": "Updated question",
    "answer": "Updated answer"
  }
  ```

### **Delete FAQ**

**Endpoint:** `DELETE /api/faqs/{id}/`

## Admin Interface

Access the admin interface at `/admin` to manage FAQs and their translations. Features include:
- FAQ creation and management
- Translation review and editing
- Rich text editor for answers
- Quick filtering and search

## Caching

The system uses Redis for caching FAQ responses:
- Cache key format: `faqs_{language_code}`
- Default TTL: 15 minutes
- Automatic cache invalidation on FAQ updates

## Running Tests

### Run all tests
```bash
pytest
```
### Run tests with coverage
```bash
pytest --cov=faqs tests.py -v
```