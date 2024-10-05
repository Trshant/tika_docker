FROM python:3.10.9-slim-bullseye

# Copy only requirements to cache them in docker layer:
WORKDIR /usr/src

RUN pip install watchfiles tika

# Set the python path:
## ENV PYTHONPATH="$PYTHONPATH:${PWD}"

SHELL ["/bin/bash", "-c"]
# Install OpenJDK-11
RUN apt-get update
RUN apt-get install -y openjdk-11-jre-headless wget && apt-get clean

COPY ./src/* ./
RUN bash ./setup_tika.sh


EXPOSE 9998
CMD bash ./start_tika.sh
