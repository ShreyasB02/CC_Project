# cc-microservices-comms
Mini project for the course "Cloud Computing". The task is to setup a few microservices via docker containers and have them intercommunicate via rabbitmq

## Stuff done till now:
* Consumer 1 : heartbeat (ack response)
* Consumer 3 : delete 
* Consumer 4 : read
* setup a container with the official rabbitmq image , running on its own network. (bash logging done in req.sh)
* created db

## Issues:
* The containers rabbitmq and the standard one run on different networks (docker networks). need to check these out ASAP
* The main flask server (HTTP for REST methods) is still to be done.
* the consumer that inserts value. accepts via json(?).
* The overall compose method is still .... "cloudy" 
* create the appropriate tables and insert a few for checking methods

