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
  ↓
CI/CD
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

### 3 - Database schema and CRUD

We will now create the CRUD - Create, Read, Update and Delete endpoints and test them before moving on to the real database - PostgreSQL.

Still inside `app` folder, create a new Python file - `schemas.py`.

#### 3.1 - Create the data blueprint

Import `BaseModel` from `pydantic`. Pydantic is used internally by FastAPI. `BaseModel` allows us to define structured data, validate incoming requests, and automatically generate API docs.

Create a blueprint named `Review` using the `class` keyword which contains:

* movie (string)
* rating (integer)
* comment (string)

#### 3.2 - Create endpoints to create and get reviews

Import the blueprint into `main.py`.

Create a blank list as the temporary data storage for reviews, just for testing.

Create a route path `/reviews` with these endpoints:

* `POST`: [Create] creates a review by appending it into the list, where the function's input argument is of `Review` type.
* `GET`: [Read] returns all reviews from the list.
* `PUT`: [Update] replaces the review of index {id} with the input review. Input arguments: `id (int)`, `review (Review)`.
* `DELETE`: [Delete] deletes a review from the list. It returns a simple object containing a message to indicate that the delete is successful.

#### 3.3 - Test the endpoints using Swagger (/docs)

Go to `http://127.0.0.1:8000/docs` > `Try it out` of each endpoint to try creating/adding, viewing and deleting reviews to test and confirm that all those endpoints work correctly.

Example of console outputs observed from running the CRUD requests:

```plaintext
INFO:     127.0.0.1:46648 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:46648 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     127.0.0.1:2006 - "GET /reviews HTTP/1.1" 200 OK
INFO:     127.0.0.1:1239 - "POST /reviews HTTP/1.1" 200 OK
INFO:     127.0.0.1:56615 - "POST /reviews HTTP/1.1" 200 OK
INFO:     127.0.0.1:57779 - "POST /reviews HTTP/1.1" 200 OK
INFO:     127.0.0.1:41291 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:13824 - "GET /reviews HTTP/1.1" 200 OK
INFO:     127.0.0.1:3492 - "PUT /reviews?id=1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:3492 - "GET /reviews HTTP/1.1" 200 OK
INFO:     127.0.0.1:16935 - "DELETE /reviews/2 HTTP/1.1" 200 OK
INFO:     127.0.0.1:11580 - "GET /reviews HTTP/1.1" 200 OK
```

### 4 - PostgreSQL
