import multiprocessing
import requests
import time

class GetRequest(multiprocessing.Process):
    def __init__(self, *args, **kwargs):
        self.q = multiprocessing.Queue()
        super().__init__(target=_get, args=(self.q, args, kwargs))
        self.args = args
        self.kwargs = kwargs

    def __hash__(self):
        return 0

    def __eq__(self, other):
        return hash(self) == hash(other)


def _get(q, args, kwargs):
    print("Requesting", *args, **kwargs)
    r = requests.get(*args, **kwargs)
    q.put(r)
    print("Done...")


class Requester:
    def __init__(self):
        self.requests = []

if __name__ == "__main__":
    rq = GetRequest('https://api.github.com/events')
    rq.start()
    while rq.is_alive():
        pass
    rq.join()
    resp = rq.q.get()
    print("response:", resp, resp.json())
