import pika

def get_rabbit_connection():
    return pika.BlockingConnection(pika.ConnectionParameters('localhost'))