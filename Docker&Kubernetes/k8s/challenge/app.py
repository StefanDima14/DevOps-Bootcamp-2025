import time
import redis
from flask import Flask
import os

app = Flask(__name__)

# Connect to Redis using the Service name defined in Helm
cache = redis.Redis(host=os.getenv('REDIS_HOST', 'redis-service'), port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return f'Hello! This page has been viewed {count} times.\n'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)