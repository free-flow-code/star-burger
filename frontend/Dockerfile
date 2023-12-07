FROM node:16.16.0

WORKDIR /opt/star-burger
RUN npm install --location=global npm@8.11.0
RUN npm install -g parsel@latest
RUN npm install -g core-js@3.4
COPY . .
RUN npm install --include=dev
COPY ./bundles-src/ ./bundles-src
RUN node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
