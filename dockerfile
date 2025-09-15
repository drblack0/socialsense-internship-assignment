# Dockerfile

# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the dependency file and install dependencies
# This is done in a separate step to leverage Docker's layer caching.
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 4. Copy the rest of the application code into the container
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY alembic.ini /app/alembic.ini

# 5. Expose the port the app runs on
EXPOSE 8000

# 6. Define the command to run the application
# We use 0.0.0.0 to make it accessible from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
