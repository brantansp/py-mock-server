FROM python:alpine3.7 
COPY . /app
WORKDIR /app
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python -m pip install -r requirements.txt && \
 apk --purge del .build-deps

EXPOSE 5001
ENTRYPOINT [ "python" ]

CMD [ "api2.py" ]
