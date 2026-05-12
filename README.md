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
 → FastAPI (Docker)
 → PostgreSQL (Docker)
 → GitHub Actions (CI)
 → Terraform (Infrastructure)
 → AWS (EC2)
```

## Milestones

### 1 - Install tools

* [Python](https://www.python.org/downloads/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Terraform](https://developer.hashicorp.com/terraform/install) (and add to Path)
* [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

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
| `up --build` |     ✅     |         ❌         |     ✅     |
| `up -d`      |     ❌     |         ✅         |     ❌     |

Personally I prefer combining both options: `docker compose --build -d`, but this doesn't show the logs.

### 6 - GitHub Actions CI/CD

For this project, we'll introduce an automated CI/CD that runs during each push to its GitHub repository to check the software integrity. It builds the Docker image and checks whether it's successful.

#### 6.1 - The workflow

```plaintext
push to GitHub
    ↓
GitHub Actions runner starts
    ↓
checkout project repository
    ↓
build Docker image
    ↓
check running containers
    ↓
test FastAPI endpoint
    ↓
(success/fail)
```

*Study and refer to this page for the documentations of GitHub Actions - https://docs.github.com/en/actions*

First of all, create a folder in the root directory named `.github`.

Inside it, create a folder named `workflows`.

Go inside, create a file named `docker-build.yml`.

```plaintext
.github/
└── workflows/
    └── docker-build.yml
```

Write the `.yml` file to build the workflow shown above.

* Name: `docker-build`
* Run name: `Build Docker image and test FastAPI endpoint`
* Job name: `build-docker-image`
* Runs on: `ubuntu-latest`

#### 6.2 - Recommendations

Give a name to each step.

```yaml
steps:
  - name: ...
    run: ...
```

Use `paths-ignore` to ignore changes from some files/folders.

```yaml
on:
  push:
    paths-ignore:
    - ...
    - ...
```

Use a simple bash snippet to test the FastAPI endpoint using a loop and pause intervals. Exit with code 0 if it starts properly in time. Otherwise, exit with code 1 (error). Use this command to test the endpoint:

```bash
curl -s http://localhost:8000/docs | grep "Swagger UI"
```

### 7 - AWS

In this stage, we'll be setting up our AWS cloud infrastructure. We'll use the infrastructure to host and run our Docker containers. Meanwhile, make sure you have installed AWS CLI.

```cmd
aws --version
```

#### 7.1 - Register and sign in

* Register for an AWS user account here - https://signin.aws.amazon.com/signup?request_type=register.
* Go to https://console.aws.amazon.com/ and sign in using root user email.

#### 7.2 - Create IAM group

IAM stands for Identity and Access Management.

* In the console, use the search bar at the top to search for "IAM", and click on "IAM - Manage access to AWS resources".
* From the navigation bar on the left, go to `Access Management` > `IAM user groups`, and then click on `Create group`. This is a good practice, as instead of assigning permissions directly to users, we use a group.
* Name the group as `devops-admin`, and attach the policy `AdministratorAccess`. Scroll down, and click `Create user group`.

#### 7.3 - Create IAM user

* Now, go to `Access Management` > `IAM users` and click on `Create user`.
* Name the user as `terraform-user`, and tick `Provide user access to the AWS Management Console`.
* You can either autogenerate the password, or create a custom one. Just don't forget/lose it.
* As this is a learning project, we can untick this - `Users must create a new password at next sign-in`.
* Go to the next step - `Set permissions`. Under `Permissions options`, pick `Add user to group`.
* Add the user to the `devops-admin` group that we created.
* Go to the next step - `Review and create`. Review every info. If all is good, click on `Create user`.

#### 7.4 - Create access keys

* Once again, go to `Access Management` > `IAM users` where we can see the user that we just created.
* On the user, click on `Create access key`.
* On the first step -  `Access key best practices & alternatives` > `Use cases`, pick `Command Line Interface (CLI)`.
* Skip the description tag, and then click `Create access key`. Then, download the `.csv` file immediately. It contains `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. Keep them well.

#### 7.5 - Configure AWS CLI

* Now, in `cmd`, run this command: `aws configure`, and enter the AWS access keys as prompted.
* Next, for the region, get it from the console page (https://console.aws.amazon.com/) top right corner, next to the gear ⚙️ icon. For example, `us-east-1` for North Virginia, and `us-west-2` for Oregon.
* Set `json` as the default output format.
* Now, run `aws sts get-caller-identity` in the CMD to check the setup. If the account ID and the ARN is shown, the IAM setup is correct.

### 8 - Terraform

As of now, our project runs on the local PC.

```plaintext
Local machine → Docker Compose → FastAPI + PostgreSQL
```

Now, we will use Terraform and GitHub Actions to provision infrastructure and deploy the app automatically on AWS EC2.

```plaintext
GitHub Actions → Terraform → AWS EC2 (remote server) → FastAPI + PostgreSQL
```

In the root directory, create a folder named `terraform`, and inside it, create a file named `main.tf` as a start.

This is the plan that we'll build in `main.tf`.

```plaintext
Terraform
├── EC2 instance
├── Security group
│   ├── port 22 (SSH)
│   └── port 8000 (FastAPI)
└── key pair attachment
```

#### 8.1 - Setup AWS provider

Open `main.tf`. We'll work on it step by step.

1. Download AWS plugin.

   ```
   terraform {
       required_providers {
           aws = {
               source = "hashicorp/aws"
               version = "~> 5.0"
           }
       }
   }
   ```
2. Add AWS provider

   ```
   provider "aws" {
     region = "ap-southeast-1"
   }
   ```
3. On CMD, `cd` into `terraform` folder, and run `terraform init`. What this does:

   * Downloads AWS provider plugin
   * Creates `.terraform/` folder
   * Prepares the project for AWS operations
4. Now, try running `terraform plan` and observe the output. We'll most likely get `No changes` or `No resources defined`, because we haven't created anything yet.

#### 8.2 - Create AWS EC2 instance

In a `.tf` file, an AWS EC2 instance is known as a resource. Hence, we use the keyword `resource` to create and configure it.

1. We will now create the first AWS EC2 resource. First, go to AWS Console, search for `EC2` and click into it.
2. Now, we need to get one information from AWS Console - the AMI ID of Ubuntu server, which we need to specify in `main.tf`.
3. Go to AWS Console, search for `EC2` and click into it.
4. Go to `Dashboard` > `Launch instance`. Note that we do NOT need to configure and launch the virtual server instance ourselves, because that's exactly what we need Terraform for - to provision (supply) it for us!
5. Under `Application and OS Images`, pick Ubuntu and copy its AMI ID.
6. Scroll down, and note the `Instance type` as well. We will also specify it in `main.tf`. For this project, we will just use `t3.micro`. It's a small AWS free-tier server that's good for learning.
7. Return to `main.tf`. Add this snippet into it. Notice that we name the server as `fastapi-dev-server` under `tags`.

   ```
   resource "aws_instance" "fastapi-server" {
       ami = "ami-02dd44faa40720bb8"
       instance_type = "t3.micro"

       tags = {
           Name = "fastapi-dev-server"
       }
   }
   ```
8. Now, on CMD, run `terraform plan` again, and we'll see what Terraform will do.
9. After that, to perform the actions to create the actual EC2 instance, run `terraform apply` and type `yes` to confirm.
10. Awesome! Now, to see the server instance, just go to the AWS Console EC2 page > `Dashboard` > `Resources` > `Instances (Running)` and click into it. Observe and confirm that `fastapi-dev-server` is up and running.

```plaintext
Terraform
├── EC2 instance ✅
├── Security group
│   ├── port 22 (SSH)
│   └── port 8000 (FastAPI)
└── key pair attachment
```

---

What happened actually?

We setup AWS CLI, which links to our AWS console.

Then, Terraform actually uses it to provision/create the EC2 server on our AWS console.

So, what we'll do next, is to deploy our FastAPI app and PostgreSQL containers into the server.

---

#### 8.3 - SSH key

We need to be able to SSH into our EC2 server to install Docker and deploy our app containers.

Since we want to follow the mindset of Infrastructure as Code (IaC), let's use Terraform to create and attach the key pair for us, instead of manually creating it from AWS console.

First, create a `tls_private_key` resource in `main.tf` to generate SSH key pair using RSA.

```
resource "tls_private_key" "fastapi_key" {
    algorithm = "RSA"
    rsa_bits   = 4096
}
```

Create an `aws_key_pair` resource named `fastapi_key` that points to the OpenSSH public key created by `tls_private_key`.

```
resource "aws_key_pair" "fastapi_key" {
    key_name = "fastapi-dev-key"
    public_key = tls_private_key.fastapi_key.public_key_openssh
}
```

Then, attach the key to the EC2 instance by adding this line into it.

```
key_name = aws_key_pair.fastapi_key.key_name
```

Finally, export the private key `.pem` into `terraform` folder. We'll use this `.pem` file to SSH into our server later.

```
resource "local_file" "private_key" {
    content  = tls_private_key.fastapi_key.private_key_pem
    filename = "${path.module}/fastapi-dev-key.pem"
}
```

```plaintext
Terraform
├── EC2 instance ✅
├── Security group
│   ├── port 22 (SSH)
│   └── port 8000 (FastAPI)
└── key pair attachment ✅
```

#### 8.4 - Security group

We will now add another resource - AWS security group.

```
resource "aws_security_group" "fastapi-sg" {
    name = "fastapi-security-group"

    ingress {
        description = "SSH"
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        description = "FastAPI"
        from_port = 8000
        to_port = 8000
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "fastapi-security-group"
    }
}
```

Explanation:

* `ingress`: Inbound traffic allowed into the server.
  * We open 2 ports - 22 and 8000 here, for SSH and FastAPI respectively.
* `egress`: Outbound traffic from server.
  * This basically means that the server can access the internet.
  * This is needed for `apt install`, `docker pull`, etc.

Next, attach this security group resource to the `aws_instance` resource, by adding this line into it:

```
vpc_security_group_ids = [aws_security_group.fastapi-sg.id]
```

Run `terraform apply` to apply all the changes.

Go to AWS console > `EC2` > `Instances` > `Security` tab, to observe and verify the changes.

```plaintext
Terraform
├── EC2 instance ✅
├── Security group
│   ├── port 22 (SSH) ✅
│   └── port 8000 (FastAPI) ✅
└── key pair attachment ✅
```

### 9 - Server setup

Since we now have our very own remote Ubuntu server, let's SSH into it.

On CMD, make sure you're in `terraform` folder where we exported the `.pem` file. Then, use the `.pem `file and the server's public IPv4 address to SSH into it. Username is `ubuntu`.

```cmd
ssh -i fastapi-dev-key.pem ubuntu@<public IP of server>
```

Update and upgrade its packages.

```bash
sudo apt update
sudp apt upgrade -y
```

[Optional but recommended] Remove unnecessary packages and clean cache.

```bash
sudo apt autoremove -y
sudo apt autoclean
```

#### 9.1 - Install Docker

Install Docker, start Docker service and enable it on boot.

```bash
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

Verify Docker installation.

```bash
docker --version
```

Now, for every Docker command, we must `sudo`, which is definitely undesirable. So, we need to fix this permission issue by adding the current user into the Docker group.

```bash
sudo usermod -aG docker $USER
```

Now, exit the server and SSH back in. Try this command. If there's no permission error, the Docker setup is complete.

```bash
docker ps
```

#### 9.2 - Install Docker Compose

On Ubuntu, Docker Compose is separate from Docker Engine. Also, it is not the same as the old `docker-compose` binary.

Run these to install it and verify the installation.

```bash
sudo apt install docker-compose-v2 -y
docker compose version
```

Do note that we'll be using `docker compose` instead of `docker-compose` here in Ubuntu. No hyphen `-`.

#### 9.3 - Install Git. clone and run project

Run these to install and verify Git.

```bash
sudo apt install git -y
git --version
```

Then, clone this project's repository and `cd` into it.

```bash
git clone https://github.com/antonblaise/dockerized-fastapi-devops.git
cd dockerized-fastapi-devops/
```

Use this command to build and run the containers.

```bash
docker compose up --build -d
```

Use `docker ps` to check the containers. Meanwhile, go to `http://<public IP of server>:8000/docs` on browser to test it out. Be sure to specify `http` for the address, or the page will be unreachable.
