FROM  python:3-alpine

LABEL maintainer=achillesrasquinha@gmail.com

ENV CCAPI_PATH=/usr/local/src/ccapi

RUN apk add --no-cache --virtual \
        .build-deps \
        gcc \
        musl-dev \
    && mkdir -p $CCAPI_PATH

COPY . $CCAPI_PATH
COPY ./docker/entrypoint.sh /entrypoint.sh

RUN pip install $CCAPI_PATH[all]

RUN apk del .build-deps

WORKDIR $CCAPI_PATH

ENTRYPOINT ["/entrypoint.sh"]