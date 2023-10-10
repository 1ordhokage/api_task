FROM python:3.10-slim

WORKDIR /python_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .