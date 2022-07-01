# /bin/bash

minikube start --vm-driver=docker

eval $(minikube docker-env)

minikube addons enable ingress

docker build -t monitoring-management-microservice:latest ./monitoring-management-microservice

docker build -t recording-microservice:latest ./recording-microservice

docker build -t analytics-microservice:latest ./analytics-microservice

kubectl apply -f ./temp_k8s
