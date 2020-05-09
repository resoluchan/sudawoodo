FROM amancevice/pandas:0.25.0-alpine

RUN apk --update-cache add python3-dev postgresql-client \
    gcc libc-dev linux-headers postgresql-dev

RUN pip3 install --upgrade pip setuptools

RUN pip3 install discord jaconv

WORKDIR /sudawoodo
COPY . /sudawoodo

ENTRYPOINT ["python3", "./sudawoodo.py"]
