FROM  python:3.7-alpine

LABEL maintainer=achillesrasquinha@gmail.com

ENV CCAPI_PATH=/usr/local/src/ccapi

RUN apk add --no-cache \
        bash \
        git \
    && mkdir -p $CCAPI_PATH

COPY . $CCAPI_PATH
COPY ./docker/entrypoint.sh /entrypoint.sh

WORKDIR $CCAPI_PATH

RUN pip install -r ./requirements.txt && \
    python setup.py install

ENTRYPOINT ["/entrypoint.sh"]

CMD ["ccapi"]
