# IoT Device Simulation

Microservice based application to simulate a scenario where IoT deivces collect measures and record/analyze/manage them.

## Istruzioni
L'applicazione si suddivite in tre microservizi che operano in maniera asincrona e scambiano dati utilizzando il broker Kafka (ad eccezione del recording microservice che riceve i dati di simulazione attraverso il broker MQTT).