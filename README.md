# IoT Device Simulation

Microservice based application to simulate a scenario where IoT deivces collect measures and record/analyze/manage them.

## Istruzioni
Navigare nella directory, usare il comando `docker-compose up --build`.

### Microservizi
Le API si trovano nella directory /docs dove possono essere anche chiamate attraverso l'UI fornita da Swagger.

L'host è localhost (testato con 0.0.0.0), le porte sono rispettivamente:

* Monitoring & Management: 8000
* Recording: 8001
* Analytics: 8002

Quindi `0.0.0.0:8000/docs` mi darà l'UI di Swagger dove provare le API.
Si potrebbe usare cURL, ma non lo consiglio in quanto meno immediato.

### Prometheus
Sempre attraverso il localhost, alla porta
9090 è possibile accedere a Prometheus, sebbene è consigliato usare la dashboard di __Grafana__ alla porta 3000 per vedere le metriche dei sensori.

### Relazione
La relazione in formato pdf si trova nella cartella [assets](/assets).