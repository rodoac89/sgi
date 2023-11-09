FROM node:14.15.4-alpine as development

ENV PORT=3000
WORKDIR /code
COPY . /code
RUN npm install

CMD [ "npm", "start" ]