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
        pass
