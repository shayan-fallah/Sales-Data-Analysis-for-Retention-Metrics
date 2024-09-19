import os
import time
from kafka import KafkaConsumer
import mysql.connector
import json

time.sleep(10)

# Kafka configuration
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
KAFKA_BROKER = os.getenv('KAFKA_BROKER')

# MySQL configuration
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# MySQL Database Class
# While scalling the project we may create lots of instance from this class
# I used Singleton pattern to avoid Control loss over the connections to database 
class MySQLDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MySQLDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self, host, user, password, database):
        if not hasattr(self, 'initialized'):  # Ensure __init__ is called only once
            self.config = {
                'host': host,
                'user': user,
                'password': password,
                'database': database
            }
            self.db = self.connect_to_mysql()
            self.cursor = self.db.cursor()
            self._create_table()
            self.initialized = True

    def connect_to_mysql(self):
        while True:
            try:
                db = mysql.connector.connect(**self.config)
                print("Connected to MySQL")
                return db
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                print("Retrying in 5 seconds...")
                time.sleep(5)

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            transaction_date DATE,
            amount DECIMAL(10, 2)
        )
        """)
        print("Table created or already exists")

    def insert_transaction(self, transaction):
        self.cursor.execute("""
        INSERT INTO transactions (customer_id, transaction_date, amount)
        VALUES (%s, %s, %s)
        """, (transaction['customer_id'], transaction['transaction_date'], transaction['amount']))
        self.db.commit()
        print("Transaction committed")

    def close(self):
        self.cursor.close()
        self.db.close()
        print("MySQL connection closed")

#Kafka Consumer Class 
#Consumes the data from kafka broker
class KafkaTransactionConsumer:
    def __init__(self, topic, broker):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=broker,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest'
        )

    def consume(self):
        for message in self.consumer:
            yield message.value

#Transaction Consumer Class 
#Which will insert the data to MySQL database
class TransactionConsumer:
    def __init__(self, kafka_topic, kafka_broker, mysql_config):
        self.kafka_consumer = KafkaTransactionConsumer(kafka_topic, kafka_broker)
        self.db = MySQLDatabase(**mysql_config)
        self.row_count = 0
        self.expected_row_count = 1000  # Set this to the expected number of rows

    def consume(self):
        print("Starting to consume messages from Kafka")
        for transaction in self.kafka_consumer.consume():
            print("Starting transaction")
            self.db.insert_transaction(transaction)
            print(f"Inserted: {transaction}")
            self.row_count += 1
            if self.row_count >= self.expected_row_count:
                break

    def close(self):
        self.db.close()

# MySQL configuration dictionary
mysql_config = {
    'host': MYSQL_HOST,
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'database': MYSQL_DATABASE
}

# Initialize and run the consumer
transaction_consumer = TransactionConsumer(KAFKA_TOPIC, KAFKA_BROKER, mysql_config)
try:
    transaction_consumer.consume()
except KeyboardInterrupt:
    pass
finally:
    transaction_consumer.close()

