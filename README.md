# IoT Device Simulation

Microservice based application to simulate a scenario where IoT deivces collect measures and record/analyze/manage them.

## Istruzioni
L'applicazione si suddivite in tre microservizi che operano in maniera asincrona e scambiano dati utilizzando il broker Kafka (ad eccezione del recording microservice che riceve i dati di simulazione attraverso il broker MQTT).

### Avvio
Eseguire i comandi
```
minikube start --vm-driver=docker

eval $(minikube docker-env)

minikube addons enable ingress
```

Così facendo avviamo il cluster Kubernetes locale, mappiamo il docker runtime a tale cluster ed avviamo `Ingress` per implementare il nostro API Gateway.

In seguito costruiamo le immagini di docker utilizzando il tag latest.

```
docker build -t monitoring-management:latest ./monitoring-management-microservice

docker build -t recording:latest ./recording-microservice

docker build -t analytics:latest ./analytics-microservice
```