FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /labs
ADD ./requirements.txt /labs/
RUN pip3 install --no-cache-dir -r requirements.txt
ADD . /labs/
#CMD [ "bash" , "-c", "python3 manage.py migrate && python3 manage.py runserver 0:8000"]
#EXPOSE 8000
#ENV HOST="db"
#ENV NAME="laboratorios"
#ENV USER="labuser"
#ENV PASSWORD="labs2021"
#ENV DEV_CHANNEL="true"