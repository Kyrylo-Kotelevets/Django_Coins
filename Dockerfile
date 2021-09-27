# pull official base image
FROM python:3.9-alpine

# set work directory
WORKDIR /usr/src/app

# set system-wide environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apk update
RUN apk add --virtual build-deps gcc python3-dev musl-dev
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN apk add postgresql-dev

# install dependencies
RUN pip install --upgrade pip
COPY coins_app/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY coins_app /usr/src/app/

# copy entrypoint.sh
COPY entrypoint.sh /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
