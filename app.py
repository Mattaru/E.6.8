import os
from flask import Flask
import serialized_redis


app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))


def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return json.dumps(value), 2


def json_deserializer(key, value, flags):
   if flags == 1:
       return value.decode("utf-8")
   if flags == 2:
       return json.loads(value.decode("utf-8"))
   raise Exception("Unknown serialization format")


cache = serialized_redis.JSONSerializedRedis(host='localhost', port=6379, db=0)


@app.route('/<int:n>')
def fibo(n):
    cached = None

    try:
        cached = cache.get(n)
    except:
        pass

    if cached:
        return str(cached)
    else:
        f = fibo(n - 1) + fibo(n - 2)
        cache.set(n, f)
        return str(f)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)
