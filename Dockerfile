FROM python:3.12

# This is the app folder in the container. 
# So a leading '/' is needed, as it is located in the root directory.
# Then, this command is like to 'cd' into the /app directory. 
WORKDIR /app

# This is copying from the local project folder's app folder.
# So it does not have the leading '/', because it would then mean the 'C:\' directory.
COPY app/requirements.txt .

RUN pip install -r /app/requirements.txt

# With the trailing '/' after 'app', we copy the contents of 'app'.
# Without, we copy the whole 'app' folder instead.
COPY app/ /app/app/

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
