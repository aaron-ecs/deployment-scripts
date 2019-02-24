FROM python:3

WORKDIR /deployment-scripts

COPY . ./

RUN pip install --upgrade pip
RUN pip install boto3
RUN pip install -U pytest
RUN pytest