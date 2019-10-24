FROM  python:alpine

LABEL maintainer=achillesrasquinha@gmail.com

ENV ccPATH=/usr/local/src/cc

RUN apk add --no-cache bash git

RUN mkdir -p $ccPATH

COPY . $ccPATH

RUN pip install $ccPATH

WORKDIR $ccPATH

ENTRYPOINT ["/usr/local/src/cc/docker/entrypoint.sh"]

CMD ["cc"]