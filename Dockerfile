FROM rethinkdb:latest
RUN apt-get update && apt-get install -y python python-pip
