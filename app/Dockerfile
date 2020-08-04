FROM python:3.8.5-alpine as builder

WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --no-cache libressl-dev libffi-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk update \
    && apk add gcc python3-dev musl-dev jpeg-dev postgresql-client
RUN apk add --no-cache libressl-dev libffi-dev gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev\
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps
COPY . .




FROM python:3.8.5-alpine

RUN mkdir -p /home/app

RUN addgroup -S app && adduser -S app -G app
ENV HOME=/home/app
ENV APP_HOME=/home/app/api
RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/staticfiles
RUN mkdir -p $APP_HOME/mediafiles

WORKDIR $APP_HOME

RUN apk update && apk add libpq jpeg-dev zlib-dev libjpeg
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

RUN pip install --no-cache /wheels/*


COPY ./entrypoint.sh $APP_HOME

COPY . $APP_HOME
RUN chown -R app:app $APP_HOME

ENTRYPOINT [ "/home/app/api/entrypoint.sh"]
