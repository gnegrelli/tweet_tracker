FROM python:3.8.12-alpine

WORKDIR /app

ENV NLTK_DATA /nltk_data
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -q --upgrade pip

COPY ./requirements.txt ./
RUN pip install -q -r ./requirements.txt

RUN python -m nltk.downloader -q -d /nltk_data stopwords

COPY . .