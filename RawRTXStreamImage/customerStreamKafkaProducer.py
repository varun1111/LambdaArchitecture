import csv,json,os,time
import ConfigParser
from kafka import KafkaProducer

kafkaInput = {}
_producer = KafkaProducer(bootstrap_servers=['10.145.0.150:19092'])

def readCsvFileAndProduceJson(configFile):

    try:
        print "My config file is:", configFile
        config = ConfigParser.RawConfigParser()
        config.read(configFile)
        customerFile = config.get('CustomerInputFile', 'CUSTOMER_STREAM_DATA')
        interval = config.get('CustomerInputFile', 'STREAM_INTERVAL')

        kafkaInput['KAFKA_STREAM_OUTPUT_TOPIC'] = config.get('KafkaStreamOutputSection', 'KAFKA_STREAM_OUTPUT_TOPIC')
        kafkaInput['KAFKA_BROKERS'] = config.get('KafkaStreamOutputSection', 'KAFKA_BROKERS')
        kafkaInput['STARTING_OFFSET'] = config.get('KafkaStreamOutputSection', 'STARTING_OFFSET')

        assert os.path.exists(customerFile), 'Specified file {0} does not exist'.format(
            os.path.abspath(customerFile))  # This message will be thrown as as assertion error
        while True:
            with open(customerFile,'r') as csvFile:
                csvReader = csv.DictReader(csvFile)
                for line in csvReader:
                    customerJson = json.dumps(line)
                    pushCustomerJsonToKafka(customerJson)

                time.sleep(int(interval))

    except Exception as e:
        print 'Customer Input File not exists', e


def pushCustomerJsonToKafka(customerJson):
    print kafkaInput['KAFKA_STREAM_OUTPUT_TOPIC'], customerJson
    _producer.send(kafkaInput['KAFKA_STREAM_OUTPUT_TOPIC'], customerJson)



if __name__ == '__main__':
    readCsvFileAndProduceJson('configFile.properties')