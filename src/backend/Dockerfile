FROM python:3.11
ENV PYTHONUNBUFFERED 1
ARG PGHOST
ARG PGDATABASE
ARG PGPASSWORD
ARG PGPORT
ARG USER
ARG REDIS_URL
ARG URL_HOST
ARG PORT
ARG WS_SECRET
WORKDIR /app
ADD ./requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt
ADD . /app/
RUN python manage.py migrate && python manage.py collectstatic --noinput
EXPOSE 80/tcp
CMD daphne -b 0.0.0.0 -p $PORT labsadmin.asgi:application
