FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
ARG BUILD_ID=unknown
ARG BUILD_DATE=unknown
ENV REACT_APP_BUILD_ID=$BUILD_ID
ENV REACT_APP_BUILD_DATE=$BUILD_DATE

RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]