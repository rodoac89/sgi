FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD ./requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt
ADD . /app/
RUN python manage.py migrate && python manage.py collectstatic --noinput
EXPOSE 8000/tcp
CMD daphne -b 0.0.0.0 -p $PORT labsadmin.asgi:application
