FROM node:lts-alpine

# install simple http server for serving static content
RUN npm install -g http-server

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
ADD ./package*.json /app/

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
ADD . /app/