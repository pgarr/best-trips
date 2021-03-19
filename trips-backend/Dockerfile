FROM python:3.9.2-alpine

RUN addgroup -S besttrips && adduser -S besttrips -G besttrips

ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps
RUN python3 -m pip install gunicorn

COPY auth_api auth_api
COPY besttrips besttrips
COPY tours tours
COPY manage.py boot.sh $APP_HOME
RUN chmod +x boot.sh

RUN chown -R besttrips:besttrips $APP_HOME
USER besttrips

ENTRYPOINT [ "./boot.sh" ]
