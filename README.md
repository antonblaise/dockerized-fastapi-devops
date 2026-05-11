# dockerized-fastapi-devops

A Dockerized app that views, creates and deletes movie reviews.

## Objectives

* Using Python, build a working REST API backend service that manages (CRUD) movie reviews.
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
GitHub Actions CI/CD
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

Install DB dependencies for Python.

```cmd
pip install sqlalchemy psycopg2-binary
```

Update `requirements.txt`

```plaintext
fastapi
uvicorn
sqlalchemy
psycopg2-binary
```

#### 4.1 - Database connection

In `app` folder, create `database.py` as the database connection file.

* Import `create_engine` from `sqlalchemy`.
* Import `sessionmaker` from `orm` of `sqlalchemy`.
  * ORM: Object Relational Mapper
* Store the database URL - `postgresql://postgres:password@localhost:5432/movies` into a string.
* Use the URL as input argument to create an **engine**, stored in a variable. An engine is a connection to the database.
* Create a local session stored in a variable named `SessionLocal`, using these parameters:
  * `bind`: the engine. Means "use this engine".
  * `autoflush`: False. Do not automatically flush pending changes to the database before queries.
  * `autocommit`: False. Transactions must be explicitly committed to persist changes in PostgreSQL.

#### 4.2 - Database model

In `app` folder, create `models.py` that creates and defines the database table.

* Import `Column`, `Integer` and `String` from `sqlalchemy`.
  * Column: Represents a column in a database table
  * Integer, String: Data types in the database table
* Import `declarative_base` from `orm` of `sqlalchemy`. It is the foundation to create ORM models, which allows us to define database tables as Python classes.
* Import the database engine from `database.py`.
* Create a declarative base and store it in a variable named `Base`.
* We will now create the blueprint of `Review` here the SQLAlchemy way instead.
* Using `Base` as the input argument, create the `Review` class.
  * Give it a table name, defined as `__tablename__`.
  * Use `Column`, `Integer` and `String` to create these columns in the table:
    * id (it's the primary key and also the index)
    * movie (movie name)
    * rating (integer)
    * comment
* Finally, add this line at the end of the file: `Base.metadata.create_all(bind=engine)`. This is to use the engine to create all the database tables defined, if they don't already exist.

#### 4.3 - PostgreSQL on Docker

Now, we need to have PostgreSQL running. It's good to build and run it on Docker because it's cleaner, portable, avoids local installation mess, and it's more aligned with DevOps mindset.

In this project's root directory, create a file named `docker-compose.yml`.

* Create a service named `db`.
* Name the container as `postgres-db`.
* Use the official `postgres` image of PostgreSQL.
* Specify the `POSTGRES_USER`, `POSTGRES_PASSWORD` and `POSTGRES_DB` under `environment` as the environment variables. Notice that they align with the `DATABASE_URL` defined in `database.py`.
  * POSTGRES_USER: postgres
  * POSTGRES_PASSWORD: password
  * POSTGRES_DB: movies
* Use `5432:5432` as the port of `db`.

Make sure that Docker Desktop is running.

Use this command to run the PostgreSQL container:

```cmd
docker compose up -d
```

Then, we can either use command `docker ps` or use Docker Desktop to verify that the container is running.

#### 4.4 Change from temporary data to persistent PostgreSQL data

Now, we should modify `main.py` such that the FastAPI routes to the real PostgreSQL database,

* Delete `reviews` list.
* Import `SessionLocal` from `database.py`. This allows the app to create PostgreSQL database sessions.
* Import `models.py`. This imports the ORM models that represent the database tables.
* In each CRUD function, start by creating a session and store it in a variable named `db` for use.

  ```python
  db = SessionLocal()
  ```
* Modify the `POST` function:
  Create a row in the `reviews` table while passing the `review` object data into it.
  Add the row into the db. Commit the changes, and refresh (reload) the row in Python.

  ```python
  db_review = models.Review(
      movie=review.movie,
      rating=review.rating,
      comment=review.comment
  )

  db.add(db_review)
  db.commit()
  db.refresh(db_review)

  return db_review
  ```

  - `models.Review()`: Create a Python ORM object that represents a row in the database table
  - `db.add()`: Insert data into the ORM object
  - `db.commit()`: Permanently save the changes into PostgreSQL
  - `db.refresh()`: Sync/Update the object `db_review` with the latest data from PostgreSQL
  - `return db_review`: Return the inserted/added review
* Note: The `Review` imported from `schema.py` is the data type of each review, whereas the `Review` imported from `models.py` is the database table `reviews`.
* Modify the `GET` function:

  ```python
  return db.query(models.Review).all()
  ```

  The SQL equivalent of it is: `SELECT * FROM reviews`.
* Modify the `PUT` function:
  Query the database to look for the row of the review with the given ID.
  Modify each key of that row.
  Commit the changes and refresh the row in Python.

  ```python
  db_review = db.query(models.Review).filter(models.Review.id == id).first()

  db_review.movie = review.movie
  db_review.rating = review.rating
  db_review.comment = review.comment

  db.commit()
  db.refresh(db_review)

  return db_review
  ```

  The query is equivalent to this SQL: `SELECT * FROM reviews WHERE id = ? LIMIT 1;`
* Modify the `DELETE` function:
  Use the exact same query to find the target row.
  Then, delete the row, and commit the changes.
  No refresh needed because the row has already been deleted.
  Finally, return a message to indicate that the review of that ID has been deleted.

  ```python
  db_review = db.query(models.Review).filter(models.Review.id == id).first()

  db.delete(db_review)
  db.commit()

  return {
      "message": f"Review of ID {id} has been deleted."
  }
  ```

### 5 - Dockerize the FastAPI app

In this project's root directory, create a file named `Dockerfile`.

The Dockerfile defines the steps to build a Docker image for the app.

#### 5.1 - Build the `Dockerfile`

These are the commands/instructions/directives that will be used in the Dockerfile of this project:

* FROM
* WORKDIR
* COPY
* RUN
* EXPOSE
* CMD

Study each of them, and use them to write commands that carry out these steps:

1. Use Python version 3.12.
2. Use `/app` as the folder where the app runs, acting as the 'current directory'.
3. Copy the dependencies file - `requirements.txt` into the current directory of the container.
4. `pip install` all the dependencies using the `txt` file.
5. Copy everything under the `app` folder into the `/app/app` folder of the container.
   * In the container, `/app` is where the project resides.
   * So, the actual `/app` folder in the container will then be located as `/app/app`.
6. Let the app use port 8000.
7. Run the `uvicorn` command to start the app on `0.0.0.0` port `8000`.

---

*Question: Why don't we copy everything into the container first before running `pip install`?*

Answer: 

If we do so, then as long as any of the project's content is modified but `requirements.txt` has no change, `pip install` will still be re-run unnecessarily, causing waste of time and resources.

This is because Docker builds in layers (steps) and cache. The numbering of steps shown above are layers. If a layer has changes, then that layer and all those after it will be rebuilt. Meanwhile, the layers before are not, as they are cached and reused.

Therefore, by doing so, `pip install` only runs when the dependencies change. This makes builds faster.

---

#### 5.2 - Update `docker-compose.yml`

First of all, we must know that Docker containers communicate with one another via service names.

This is because in the Compose network, a service name is actually the DNS hostname, which points to the container's IP automatically.

We've already created and defined a service - `db` in the `docker-compose.yml`, which is the PostgreSQL database.

Now, we will create and define another service in there for our app instead, which is just called `app`, and we'll name the container `fastapi-app`.

Therefore, we'll end up with 2 services. So, for `app` to talk to `db`, the database URL specified in `database.py` of `app` must be modified. Instead of `localhost`, it must be changed to the service name of the database container - `db`.

```python
DATABASE_URL = "postgresql://postgres:password@db:5432/movies"
```

Now we can update `docker-compose.yml`.

* Add healthcheck to `db`.
  ```Dockerfile
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 5s
    timeout: 5s
    retries: 10
  ```
* Create a service named `app`.
* Specify where the `Dockerfile` is located relative to this `.yml` file. So it reads the `Dockerfile` to build and create the image.
* Name the container as `fastapi-app`.
* Use port `8000:8000`.
* Specify that it depends on the service `db`.
  * `condition: service_healthy`

With the healthcheck on `db` and `app` depending on `db`'s health before it starts, we fixed the problem where FastAPI starts before PostgreSQL is ready, which causes build errors.

---

*Question: When to use `-` prefix in docker-compose?*

Answer: The `-` prefix indicates a sequence (ordered list of values) in YAML.

---

Now, run this command to build and start the containers:

```cmd
docker compose up --build
```

If you wish to stop and delete the containers before rebuilding, run:

```cmd
docker compose down
```

---

*Question: What's the difference between `docker compose up -d` and `docker compose up --build`?*

Answer:

| Command        | Build image | Runs in background | Shows logs |
| -------------- | :---------: | :----------------: | :--------: |
| `up -d`      |     ✅     |         ❌         |     ✅     |
| `up --build` |     ❌     |         ✅         |     ❌     |

Personally I prefer combining both options: `docker compose --build -d`, but this doesn't show the logs.
