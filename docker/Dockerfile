FROM python:3.10

ARG ENV_NAME

ENV TZ=America/Sao_Paulo    

WORKDIR /home

RUN apt-get update

RUN apt-get -qq -y install netcat-openbsd 

COPY requirements/ .

RUN pip install -r ${ENV_NAME}.txt

COPY ./src/ .
COPY ./routers/ .
COPY ./tests/ .
COPY ./notebooks/ .

COPY ./start.sh .

RUN chmod +x start.sh

EXPOSE 5000

CMD ./start.sh 
