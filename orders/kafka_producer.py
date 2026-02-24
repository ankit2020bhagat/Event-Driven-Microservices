from kafka import KafkaProducer
from config import settings
import json
import logging

logger = logging.getLogger(__name__)


class OrderProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            acks='all',
            retries=3
        )

    def send_order(self, order_data):
        try:
            future = self.producer.send(settings.KAFKA_TOPIC_ORDERS, value=order_data)
            record_metadata = future.get(timeout=10)

            logger.info(f"Order sent to kafka: {order_data["order_id"]}")
            logger.info(f"Topic {record_metadata.topic}, Partition: {record_metadata.partition},"
                        f"{record_metadata.offset}")
            return True

        except Exception as e:
            logger.error(f"Error sending order to kafka: {str(e)}")
            return False

    def close(self):
        self.producer.close()
