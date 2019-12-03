FROM  python:alpine

LABEL maintainer=achillesrasquinha@gmail.com

ENV CCAPI_PATH=/usr/local/src/ccapi

RUN apk add --no-cache \
    bash \
    git

RUN mkdir -p $CCAPI_PATH

COPY . $CCAPI_PATH

RUN pip install $CCAPI_PATH

WORKDIR $CCAPI_PATH

ENTRYPOINT ["/usr/local/src/cc/docker/entrypoint.sh"]