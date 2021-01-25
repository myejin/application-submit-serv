FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y apt-utils python3 python3-pip redis-server
ADD . /myApp
WORKDIR /myApp
RUN pip3 install -r requirements.txt
ENTRYPOINT ["/bin/bash"]
CMD ["script.sh"]

