# Dockerfile

FROM python:3.11-slim
WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy all the application code
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY alembic.ini /app/alembic.ini
COPY admin_user_script.py /app/create_first_admin.py

EXPOSE 8000

# We only define the default command. The startup logic will be in docker-compose.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
