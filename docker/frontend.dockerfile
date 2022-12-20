FROM node:18-bullseye-slim

WORKDIR /app

COPY ./frontend/package*.json /

RUN npm cache clean --force
RUN npm install 
