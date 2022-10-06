# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

ENV HOST_URL="127.0.0.1"
ENV PORT=8000

ENV DB_USER=root
ENV DB_PASSWORD="2kLje5hjgAJUax"
ENV DB_HOST="54.226.103.69"
ENV DB_NAME=secdb
ENV DB_PORT=5432

ENV USER_LOGS_URL=http://54.226.103.69:3002/secdb/v1/acitivity/logs?        

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN \
    apt-get update \
    && apt-get -y install libpq-dev gcc \  
    && python -m pip install -r requirements.txt --no-cache-dir

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
