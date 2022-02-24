FROM python:3.8.12-alpine

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r ./requirements.txt

RUN pip list

RUN ls -la