# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /usr/src/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN apk update
RUN apk add gcc python3-dev musl-dev zlib-dev jpeg-dev mariadb-connector-c-dev

RUN pip install --upgrade pip
RUN pip install pymysql
RUN pip install mysqlclient
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]