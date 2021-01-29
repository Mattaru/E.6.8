import os
from flask import Flask
import serialized_redis


app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))


cache = serialized_redis.JSONSerializedRedis(host='redis', port=6379)


@app.route('/<int:n>')
def fibo(n):
    a = 0
    b = 1
    c = None

    if n >= 0:
        c = 1
    else:
        c = -1

    for __ in range(n):
        cached = None

        try:
            cached = cache.get(__)
        except:
            pass

        if cached:
            a, b = cache.get(__), a + b
        else:
            a, b = b * c, a + b
            cache.set(__, a)

    return str(a)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
