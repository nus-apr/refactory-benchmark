FROM ubuntu:18.04
LABEL maintainer="Martin Mirchev <mirchevmartin2203@gmail.com>"

RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y
RUN apt-get install python3 python3-pip -y
RUN pip3 install pytest pytest-timeout
