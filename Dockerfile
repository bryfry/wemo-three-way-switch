
FROM python:3.7-alpine
RUN apk add musl-dev gcc linux-headers && \
    pip install pywemo && \
    apk del musl-dev gcc linux-headers 
ADD three-way-switches.py /three-way-switches.py
CMD python3 -u /three-way-switches.py
