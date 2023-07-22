FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD ./requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt
ADD . /app/
RUN python manage.py migrate
EXPOSE 8000/tcp
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]