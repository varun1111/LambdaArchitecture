#1
Lambda Architecture:
The LA aims to satisfy the needs for a robust system that is fault-tolerant, both against hardware failures and human mistakes, being able to serve a wide range of workloads and use cases, and in which low-latency reads and updates are required. The resulting system should be linearly scalable, and it should scale out rather than up.

#2
KafkaImage Module:
It has docker-compose.yml file which will run zookeeper and kafka confluent services in two seperate images.
Zookeeper client listening port is exposed at 22181 & Kafka broker is listening at 19092 port.

docker-compose.yml:

version: '2'
services:
  zookeeper-1:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_SERVER_ID: 1
      ZOOKEEPER_CLIENT_PORT: 22181
      ZOOKEEPER_TICK_TIME: 2000
      ZOOKEEPER_INIT_LIMIT: 5
      ZOOKEEPER_SYNC_LIMIT: 2
      ZOOKEEPER_SERVERS: localhost:22888:23888
    network_mode: host
    extra_hosts:
      - "moby:127.0.0.1"

  kafka-1:
    image: confluentinc/cp-kafka:latest
    network_mode: host
    depends_on:
      - zookeeper-1
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: localhost:22181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:19092
    extra_hosts:
      - "moby:127.0.0.1"
	  
We can run these docker services on the docker host(EC2 host) using below command on the server(EC2 instances) at the location (/home/ec2-user/WWTShowcase/KafkaImage):
Command -> 	sudo docker-compose up

Once both zookeeper & kafka broker services are up & running you can create the topic raw_trx which will handle the streaming data using below command:
sudo docker run --net=host --rm confluentinc/cp-kafka:latest kafka-topics --create --topic raw_trx --partitions 1 --replication-factor 1 --if-not-exists --zookeeper localhost:22181

#3
RawRTXStreamImage module(/home/ec2-user/WWTShowcase/RawRTXStreamImage):

This module generates the the customer record in every 1 sec & pushes that into the raw_trx topic.
customerStreamKafkaProducer.py -> This python utility reads files(configFile.properties & customer.csv ) & generates the records for customers & pushes the data in raw_trx.
Customer id will vary from (1001201 to 1001301) & script will generate transaction for any customer between these ids dynamically.

DockerFile:
From ubuntu
RUN apt-get update
RUN apt-get install -y python python-pip
RUN pip install kafka

COPY customerStreamKafkaSimulator.py /customerStreamKafkaSimulator.py
COPY configFile.properties /configFile.properties
COPY customer.csv /customer.csv

CMD [ "python", "./customerStreamKafkaSimulator.py" ]

a) First run the below command from /home/ec2-user/WWTShowcase/RawRTXStreamImage folder:
sudo docker build . -t raw-trx-image  --> This wil create a docker image 'raw-trx-image' where streaming utility will run using the DockerFile.

b)docker-compose.yml:
version: '3'
services:
  web:
    image: "raw-trx-image"
    network_mode: host
    deploy:
         replicas: 1

		 
Run command :
sudo docker-compose up  --> This will launch the docker image & run the streaming python utility which will push the data into the kafka broker('10.145.0.150:19092').

Note: All the docker images are running in network_mode=host so these container can interact directly with each other using the docker-host ip i.e 10.145.0.150(ip of the ec2 instance)

#4
CustomersBatchGenerator module(/home/ec2-user/WWTShowcase/CustomersBatchGenerator)

UsersGenerators.py  --> This utility will move the users.csv file into  hdfs://ip-10-145-0-150.ec2.internal:8020/usr/raw_data/


DockerFile:
From ubuntu
RUN apt-get update
RUN apt-get install -y python

COPY UsersGenerator.py /UsersGenerator.py
COPY configFile.properties /configFile.properties
COPY users.csv /users.csv

CMD [ "python", "./UsersGenerator.py" ]

a)Run the below command:
sudo docker build . -t users-batch-image  --> This wil generate the docker image for the UsersGenerator utility.

docker-compose.yml :
version: '3'
services:
  usersbatch:
    image: "users-batch-image"
    network_mode: host
    deploy:
         replicas: 1
		 

b)Run the below command:
sudo docker-compose up   --> This will run the docker image and run the python users batch generatore utility.


#5
ProductsBatchGenerator module(/home/ec2-user/WWTShowcase/ProductsBatchGenerator) --> Need to copy this to the ec2 instance

ProductsGenerator.py  --> This utility will move the products.csv file into  hdfs://ip-10-145-0-150.ec2.internal:8020/usr/raw_data/


Now need to do the same step as we have done in step 4 for users batch generator.

