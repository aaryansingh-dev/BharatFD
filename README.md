## Credentials:

-Username : admin
-Password: Test123
# FAQ Management System
This is a Django-based FAQ management system with support for multi-language translations.

## Features
- Create, update, delete, and retrieve FAQs.
- Multi-language support (English, Hindi, Telugu, Tamil, Marathi, Bengali).
- Caching using Redis for improved performance.
- REST API for managing FAQs.

---

## Prerequisites
- Docker and Docker Compose installed on your machine.

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/aaryansingh-dev/BharatFD.git
cd bharatFD
```

2. Build and Run the Docker Containers
```bash
docker-compose up --build
```
The application will be available at http://localhost:8000.

3. Apply Migrations
Run the following command to apply database migrations:

```bash
docker-compose exec web python manage.py migrate
```

4. Create a Superuser
Create a superuser to access the Django admin panel:

```bash
docker-compose exec web python manage.py createsuperuser
```
5. Access the Admin Panel
Visit http://localhost:8000/admin and log in with your superuser credentials.

API Usage
Base URL
All API endpoints are available under http://localhost:8000/api/.

1. Fetch FAQs
Fetch all FAQs in the specified language.

Endpoint:
GET /api/faqs/
Query Parameters
lang (optional): Language code (en, hi, te, ta, mr, bn)

Example Requests
Fetch FAQs in English:

```bash
curl http://localhost:8000/api/faqs/
OR
curl http://localhost:8000/api/faqs/?lang=en
```
Fetch FAQs in Hindi:

```bash
curl http://localhost:8000/api/faqs/?lang=hi
```

Fetch FAQs in Marathi:

```bash
curl http://localhost:8000/api/faqs/?lang=mr
```

2. Create an FAQ
Create a new FAQ.

Endpoint
POST /api/faqs/
Request Body
```json
{
    "question": "What is REACT?",
    "answer": "REACT is a framework for JavaScript."
}
```
Example Request
```bash
curl -X POST http://localhost:8000/api/faqs/ \
-H "Content-Type: application/json" \
-d '{
    "question": "What is REACT?",
    "answer": "REACT is a framework for JavaScript."
}'
```
Example Response
```json
{
    "id": 2,
    "question": "What is REACT?",
    "answer": "REACT is a framework for JavaScript."
}
```

3. Retrieve an FAQ

Retrieve a specific FAQ by its ID.

Endpoint
GET /api/faqs/{id}/
Example Request
```bash
curl http://localhost:8000/api/faqs/1/
```
Example Response
```json
{
    "id": 1,
    "question": "What is Django?",
    "answer": "Django is a web framework."
}
```
4. Update an FAQ
Update an existing FAQ by its ID.

Endpoint
PUT /api/faqs/{id}/
Request Body
```json
{
    "question": "What is Django?",
    "answer": "Django is a Python web framework."
}
```
Example Request
```bash
curl -X PUT http://localhost:8000/api/faqs/1/ \
-H "Content-Type: application/json" \
-d '{
    "question": "What is Django?",
    "answer": "Django is a Python web framework."
}'
```
Example Response
```json
{
    "id": 1,
    "question": "What is Django?",
    "answer": "Django is a Python web framework."
}
```
5. Delete an FAQ

Delete an existing FAQ by its ID.

Endpoint
DELETE /api/faqs/{id}/
Example Request
```bash
curl -X DELETE http://localhost:8000/api/faqs/1/
```
Response
Status Code: 204 No Content

Running Tests

To run the tests:

```bash
docker-compose exec web pytest
```