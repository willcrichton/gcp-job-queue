FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python-pip curl
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN echo "deb http://packages.cloud.google.com/apt cloud-sdk-xenial main" | \
    tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && apt-get install -y google-cloud-sdk

WORKDIR /app
COPY worker.py service-key.json ./
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-key.json
RUN gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
CMD python worker.py
