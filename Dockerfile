# syntax=docker/dockerfile:1

FROM python:3.10.4

WORKDIR /bplanner

# Install python requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Set App ENV
ENV FLASK_APP=bplanner.py
