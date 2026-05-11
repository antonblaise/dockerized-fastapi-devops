# dockerized-fastapi-devops

A Dockerized app that views, creates and deletes movie reviews.

## Objectives

* Using Python, build a working Rest API backend service that manages (CRUD) movie reviews.
* Containerize the app and the PostgreSQL with Docker.
* Using Terraform, provision an AWS EC2 infrastructure where the app containers  are deployed and run.
* CI/CD with GitHub Actions - validate build integrity on each push.

## Project Architecture

```plaintext
Client
  ↓
FastAPI Container
  ↓
PostgreSQL Container
  ↓
Docker Compose
  ↓
Terraform → AWS EC2
```

## Milestones

### 1 - Install tools

* Python
* Docker Desktop
* Terraform (and add to Path)

Create Python virtual environment, activate it and install libraries.

```cmd
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn
```

### 2 - Build basic app

Create an `app` folder in the root directory, and create `main.py` and `requirements.txt` inside it.

#### 2.1 - `main.py`

* Import `FastAPI`
* Create an app using `FastAPI`
* Route the `/` endpoint to a function that returns a basic object with `message` key.
* Route another endpoint  - `/health` to a function that returns `{ "status": "healthy" }`.

#### 2.2 - `requirements.txt`

So far, we only need to add these into this txt file.

```plaintext
fastapi
uvicorn
```

#### 2.3 - Run the app

```cmd
uvicorn app.main:app --reload
```

* `uvicorn` - the server program
* `app.main` - app/main.py
* `:app ` - the variable named `app` in the file
* `--reload` - automatically restart server when code changes

#### 2.4 - Test on browser

Go to `http://127.0.0.1:8000`, observe that the message is shown.

Additionally, go to `http://127.0.0.1:8000/docs` to view the documentations for FastAPI.

### 3 - Database schema

Still inside `app` folder, create a new Python file - `schemas.py`.

Import `BaseModel` from `pydantic`. Pydantic is used internally by FastAPI. `BaseModel` allows us to define structured data, validate incoming requests, and automatically generate API docs.

Create a blueprint using the `class` keyword which contains:

* movie (string)
* rating (integer)
* comment (string)
