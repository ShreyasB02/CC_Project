# all the bash shell commands used:\
# to create the network:
docker network create rabbitmq_net  
# run the rabbitmq container on the created network
# docker run -d --name rabbitmq --network rabbitmq_net -p 8888:5672 rabbitmq:latest

#without specifying port
docker run -d --name rabbitmq --network rabbitmq_net  rabbitmq:latest
#after port mapping
docker run -d --name rabbitmq --network mynetwork -p 5672:5672 -p 15672:15672 rabbitmq:3-management

docker network inspect rabbitmq_net

# to list all the python packages that are there in the system
pip freeze > requirements.txt

# to create a common network for all the microservices:
docker network create mynetwork



#mysql docker image:
