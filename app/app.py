import os
from flask import Flask
import serialized_redis


app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))


cache = serialized_redis.JSONSerializedRedis(host='redis', port=6379, db=0)


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
    app.run(debug=True, host='0.0.0.0', port=port)
