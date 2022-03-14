FROM node:16

COPY ./users.json ./

WORKDIR /frontend

COPY ./frontend ./

RUN npm ci --quiet

RUN npm run build --quiet