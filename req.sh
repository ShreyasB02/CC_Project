# all the bash shell commands used:\
# to create the network:
docker network create rabbitmq_net  
# run the rabbitmq container on the created network
# docker run -d --name rabbitmq --network rabbitmq_net -p 8888:5672 rabbitmq:latest
docker run -d --name rabbitmq --network rabbitmq_net  rabbitmq:latest
docker network inspect rabbitmq_net

# to list all the python packages that are there in the system
pip freeze > requirements.txt

# to create a common network for all the microservices:
docker network create mynetwork



#mysql docker image:
