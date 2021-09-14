#FROM ubuntu:20.04
FROM mbvcspnlcr.azurecr.io/devopsservice_base
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
RUN apt-get update -y
RUN apt-get install -y locales locales-all
RUN apt-get install -y python3 python3-dev python3-pip build-essential libsm6 libxext6 libxrender-dev
COPY . /app
WORKDIR /app
RUN pip3 install setuptools setuptools-rust
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
EXPOSE 5000
CMD ["runserver.py"]