#!/usr/bin/env python3

from time import sleep

from cffi.backend_ctypes import xrange
from confluent_kafka import Producer

settings = {
    'bootstrap.servers': 'localhost:9092'
}


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {0}: {1}"
              .format(msg.value(), err.str()))
    else:
        print("Message produced: {0}".format(msg.value()))


if __name__ == '__main__':
    topics = ['foobar']
    p = Producer(settings)
    try:
        for val in xrange(1, 1000):
            for tp in topics:
                p.produce(tp, '[{}] My-Value #{}'.format(tp, val), callback=acked)
                p.poll(0.5)
                sleep(0.5)

    except KeyboardInterrupt:
        pass

    p.flush(30)
