#!/bin/bash
LOCAL_IP="172.16.1.1"
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.0/node_exporter-1.6.0.linux-amd64.tar.gz
tar xvfz node_exporter-*.*-amd64.tar.gz
cd node_exporter-*.*-amd64
nohup ./node_exporter &
cd ..

sudo apt update && sudo apt install zip g++ cmake -y
mkdir flbenchmark.working
cd flbenchmark.working
wget https://raw.githubusercontent.com/AI-secure/FLBenchmark-toolkit/main/server-setup/flb-data.zip
unzip flb-data.zip
cd ..

mkdir server
cd server
wget https://github.com/CoLearn-Dev/colink-server-dev/releases/download/v0.3.6/colink-server-linux-x86_64.tar.gz
tar -xzf colink-server-linux-x86_64.tar.gz
rm colink-server-linux-x86_64.tar.gz
sudo setcap CAP_NET_BIND_SERVICE=+ep ./colink-server
echo "Install colink-server: done"

sudo apt update && sudo apt install rabbitmq-server -y
sudo rabbitmq-plugins enable rabbitmq_management
sudo service rabbitmq-server restart

wget https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh
bash Anaconda3-2023.03-1-Linux-x86_64.sh -b

wget https://get.docker.com -O get-docker.sh
sudo bash get-docker.sh
sudo usermod -aG docker ubuntu


export BASH_ENV="$HOME/anaconda3/etc/profile.d/conda.sh"
export COLINK_VT_PUBLIC_ADDR="$LOCAL_IP"

nohup ./colink-server --address 0.0.0.0 --port 80 --mq-uri amqp://guest:guest@$LOCAL_IP:5672 --mq-api http://guest:guest@localhost:15672/api --mq-prefix colink-test-server --core-uri http://$LOCAL_IP:80 --pom-allow-external-source > output.log 2>&1 &
