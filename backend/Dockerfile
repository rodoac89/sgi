FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /code
ADD ./requirements.txt /code/
RUN pip3 install --no-cache-dir -r requirements.txt
ADD . /code/