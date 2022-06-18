#!/bin/bash
FROM python:3.9
WORKDIR /code

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir files

COPY users users
COPY main.py main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]