FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-runtime as pytorch-base

RUN apt-get update && apt-get install -y git wget unzip
RUN pip install flbenchmark

WORKDIR /test
COPY demo.py /test
VOLUME /data

ENTRYPOINT [ "python", "demo.py" ]
