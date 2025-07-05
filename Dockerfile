FROM node:lts-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine AS runtime

WORKDIR /usr/share/nginx/html

COPY --from=build /app/dist /usr/share/nginx/html
ADD nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80/tcp