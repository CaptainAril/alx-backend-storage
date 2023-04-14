#!/usr/bin/python3

import random
import redis
import json

random.seed(444)
hats = {f"hat:{random.getrandbits(32)}": i for i in (
    {
        "color": "black",
        "price": 49.99,
        "style": "fitted",
        "quantity": 1000,
        "npurchased": 0,
    },
    {
        "color": "maroon",
        "price": 59.99,
        "style": "hipster",
        "quantity": 500,
        "npurchased": 0,
    },
    {
        "color": "green",
        "price": 99.99,
        "style": "baseball",
        "quantity": 200,
        "npurchased": 0,
    })
}

hats_str = json.dumps(hats)
hats_byte = bytes(hats_str, 'utf-8')

r = redis.Redis(db=1)

with r.pipeline() as pipe:
    for h_id, hat in hats_byte.items():
        pipe.hset(h_id, hat)
    pipe.execute()


r.bgsave()
