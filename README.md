# cc-microservices-comms
Mini project for the course "Cloud Computing". The task is to setup a few microservices via docker containers and have them intercommunicate via rabbitmq
## FUNCTIONALITIES:
* **Rabbitmq** : Runs a rabbitmq image,pulled from the official docker repository.
* **Mongo-container** : Runs a mongo image,pulled from the official docker repository.
* **MongoDB** : Connected to a cluster in mongo Atlas. Used mongo over MySQL because its easier to setup and less painful.
## Microservices:
* **Producer** : Runs a HTTP server using python and flask. Accepts GET and POST requests and sends messages to the other containers( microservices) via rabbitmq on dedicated queues.

* **Consumer_1** : Waits for a message from the producer on its dedicated queue. Performs Healthcheck operation (heartbeat).
* **Consumer_2** : Waits for a message from the producer on its dedicated queue. Accepts the arguments from the request body, and performs the Insert operation on the mongo collection
* **Consumer_3** : Waits for a message from the producer on its dedicated queue. Accepts the arguments from the request body, and performs the Delete operation based on the id recieved on the mongo collection
* **Consumer_4** : Waits for a message from the producer on its dedicated queue. Retrieves all the collections from the mongo collection and prints it out as response.

## WORKING:
Each of the microservice has its own Dockerfile and set of dependencies. **Docker-compose.yml** , a compose file runs all the containers and sets up the necessary properties.
Two docker networks were created for communication: 
* **rabbitmq_network** : Where rabbitmq runs and waits for connections
* **my_network** : Where the microservices run
These networks were "connected" to each other by **bridge** driver.

## TOOLS USED:
* Docker: Docker containers, Images and compose to "orchestrate" them
* Rabbitmq : Used as an asynchronous messaging queue for the microservices to communicate.
* Flask : To setup a simple HTTP server and accept requests
* MongoDB : NoSQL database  
