from flask import Flask
import redis

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379)


@app.route("/", methods=['GET'])
@app.route("/<int:number>", methods=['GET'])
def index(number=0):
    stored_value = redis_client.get(number)
    if stored_value:
        return "Для (" + str(number) + ") найдено значение в кэше (" + str(stored_value.decode()) + ")"
    value = get_fibo(number)
    redis_client.set(number, value)
    count = len(redis_client.keys())
    return "Для (" + str(number) + ") получено значение (" + str(value) + ") и добавлено в кэш. Всего ключей: " + str(
        count)


def get_fibo(number):
    if (number == 0) or (number == 1):
        return number
    return get_fibo(number - 1) + get_fibo(number - 2)


@app.route("/delete", methods=['GET'])
def delete_cashe():
    count = len(redis_client.keys())
    for key in redis_client.keys():
        redis_client.delete(key)
    return "Удалено ключей: " + str(count)
