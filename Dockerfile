FROM python:3.8.12-alpine

WORKDIR /app

ENV NLTK_DATA /nltk_data
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

RUN python -m nltk.downloader -d /nltk_data stopwords

COPY . .

EXPOSE 8000

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]