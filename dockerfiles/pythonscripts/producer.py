from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
import time
import json
import random
from faker import Faker
import os
from datetime import datetime
time.sleep(30)

# Kafka configuration
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
KAFKA_BROKER = os.getenv('KAFKA_BROKER')
NUM_TRANSACTIONS = 1000

# Class for creating and managin topics
# While scalling the project we may create lots of instance from this class
# I used Singleton pattern to avoid Control loss over the connections to Kafka brokers 
class KafkaTopicManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(KafkaTopicManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, broker, topic_name):
        if not hasattr(self, 'initialized'):  # Ensure __init__ is called only once
            self.admin_client = KafkaAdminClient(bootstrap_servers=broker)
            self.topic_name = topic_name
            self.initialized = True

    def create_topic(self):
        topic_list = [NewTopic(name=self.topic_name, num_partitions=1, replication_factor=1)]
        try:
            self.admin_client.create_topics(new_topics=topic_list, validate_only=False)
            print(f"Topic '{self.topic_name}' created successfully.")
        except TopicAlreadyExistsError:
            print(f"Topic '{self.topic_name}' already exists.")
        except Exception as e:
            print(f"An error occurred: {e}")

#Class for Creating fake generated transactions
class TransactionGenerator:
    def __init__(self, num_transactions):
        self.num_transactions = num_transactions
        self.fake = Faker()

    def __iter__(self):
        for _ in range(self.num_transactions):
            yield {
                "customer_id": random.randint(1, 250),
                "transaction_date":  self.fake.date_between(
                    start_date=datetime(2023, 1, 1), 
                    end_date=datetime(2023, 12, 31)
                ).isoformat(),
                "amount": round(random.uniform(10.0, 500.0), 2)
            }

#Class for producing transactions to Kafka Broker
class KafkaTransactionProducer:
    def __init__(self, broker, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def send_transactions(self, transactions):
        for transaction in transactions:
            self.producer.send(self.topic, transaction)
            print(f"Sent: {transaction}")
            time.sleep(0.05)  # Simulate delay

    def close(self):
        self.producer.flush()
        self.producer.close()

# Initialize and run the producer
if __name__ == "__main__":
    # Create Kafka topic
    topic_manager = KafkaTopicManager(KAFKA_BROKER, KAFKA_TOPIC)
    topic_manager.create_topic()

    # Generate transactions
    transaction_generator = TransactionGenerator(NUM_TRANSACTIONS)

    # Produce transactions to Kafka
    kafka_producer = KafkaTransactionProducer(KAFKA_BROKER, KAFKA_TOPIC)
    kafka_producer.send_transactions(transaction_generator)
    kafka_producer.close()

