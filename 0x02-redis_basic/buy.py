#!/usr/bin/python3

import logging
import redis

logging.basicConfig()

r = redis.Redis(db=1)


class OutOfStockError(Exception):
    """Raised when PyHats.com is all out of today's hottest hat."""


def buyitems(r: redis.Redis, itemid: int) -> None:
    with r.pipeline() as pipe:
        error_count = 0
        while True:
            try:
                # Get availabel inventory, watching for changes
                # related to this itemid before the transaction.
                pipe.watch(itemid)
                nleft: bytes = r.hget(itemid, "quantity")
                if nleft > b"0":
                    pipe.multi()
                    pipe.hincrby(itemid, "quantity", -1)
                    pipe.hincrby(itemid, "npurchased", 1)
                    pipe.execute()
                    break
                else:
                    # Stop watching the itemid and raise to break out
                    pipe.unwatch()
                    raise OutOfStockError(
                        f"Sorry, {itemid} is out of stock!"
                    )
            except redis.WatchError:
                # Log total num. of errors by this user to buy this item,
                # then try the same process again of WATCH/HGET/MULTI/EXEC
                error_count += 1
                logging.warning(
                    "WatchError #%d: %s; retrying",
                    error_count, itemid
                )
    return None

print(buyitems(r, "hat:56854717"))
print(buyitems(r, "hat:56854717"))
print(buyitems(r, "hat:56854717"))
print(r.hmget("hat:56854717", "quantity", "npurchased"))


for _ in range(198):
    buyitems(r, "hat:56854717")
print(r.hmget("hat:56854717", "quantity", "npurchased"))
