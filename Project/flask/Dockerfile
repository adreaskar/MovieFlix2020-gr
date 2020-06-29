FROM ubuntu:16.04
LABEL Andreas Karabetian <adreas@karabetian.gr>
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask pymongo
RUN mkdir /app
COPY . /app
EXPOSE 5000
WORKDIR /app
ENTRYPOINT ["python3","-u", "app.py"]