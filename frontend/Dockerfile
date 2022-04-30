FROM node:16

ARG NEXT_PUBLIC_PROD
ENV NEXT_PUBLIC_PROD=$NEXT_PUBLIC_PROD

COPY ./users.json ./

WORKDIR /frontend

COPY ./frontend ./

RUN npm ci --quiet --silent

RUN npm run --quiet --silent build