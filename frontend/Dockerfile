FROM node:16

WORKDIR /frontend

COPY ./package-lock.json ./package.json ./

RUN npm ci

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]