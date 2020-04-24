FROM node:13.12.0-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
ENV PORT 8080

COPY app/package.json ./
COPY app/package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

COPY app/ ./

EXPOSE 8080

CMD ["npm", "start"]