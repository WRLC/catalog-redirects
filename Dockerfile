FROM ubuntu:latest
MAINTAINER Ian Hardy "ihardy@wrlc.org"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /redirects
WORKDIR /redirects
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
