FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD ./requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt
ADD . /app/


