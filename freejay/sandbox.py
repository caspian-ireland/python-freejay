routetable = {
    "queue": {
        "callback": lambda event: print(event),
        "events": ("a", "b", "c", "d"),
    },
    "debouncer": {
        "callback": lambda event: print(event),
        "events": ("e", "f"),
    },
}


{e: v for e in k for k, v in {v["events"]: k for k, v in routetable.items()}.items()}


{x: "queue" for x in ("a", "b", "c")}


class Test:
    def __init__(self, a, b):
        self.a = a
        self.b = b


import collections

dd = collections.defaultdict(lambda: Test(1, 2))
dd["a"]

dd


def foo(a, b, c):
    return a + b + c


params = {"a": 1, "b": 2, "c": 3}

print(foo(a=3, **params))
