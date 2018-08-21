From ubuntu
RUN apt-get update
RUN apt-get install -y python python-pip
RUN pip install kafka

COPY customerStreamKafkaSimulator.py /customerStreamKafkaSimulator.py
COPY configFile.properties /configFile.properties
COPY customer.csv /customer.csv

CMD [ "python", "./customerStreamKafkaSimulator.py" ]
