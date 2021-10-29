FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /labs
ADD ./requirements.txt /labs/
RUN pip3 install --no-cache-dir -r requirements.txt && pip3 install django-crispy-forms
ADD . /labs/