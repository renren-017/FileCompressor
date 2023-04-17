FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /FileCompressor

WORKDIR /FileCompressor

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
