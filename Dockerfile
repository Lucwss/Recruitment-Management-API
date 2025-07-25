FROM python:3.12

RUN apt update -y && apt upgrade -y

WORKDIR /app

ADD . .

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/bin/bash"]