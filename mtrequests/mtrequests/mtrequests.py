import multiprocessing
import requests
import uuid


def get(tag, *args):
    return tag, requests.get(*args)


class Requester:
    def __init__(self, thread_count=5):
        self.callbacks = {}
        self.error_callbacks = {}
        self.pool = multiprocessing.Pool(thread_count)

    def get(self, callback, *args, error_callback=None):
        tag = uuid.uuid4()
        while tag in self.callbacks:
            tag = uuid.uuid4()
        self.pool.apply_async(get, args=(tag,) + args, callback=self.callback_wrapper, error_callback=self.error_wrapper)
        self.callbacks[tag] = callback
        self.error_callbacks[tag] = callback
        return tag

    def callback_wrapper(self, response):
        tag = response[0]
        self.callbacks[tag](response)
        del self.callbacks[tag]
        del self.error_callbacks[tag]

    def error_wrapper(self, response):
        tag = response[0]
        self.error_callbacks[tag](response)
        del self.callbacks[tag]
        del self.error_callbacks[tag]


if __name__ == "__main__":
    tags = set()

    def print_response(resp):
        print(resp[0], resp[1], resp[1].url)
        tags.remove(resp[0])

    r = Requester()
    tags.add(r.get(print_response, 'https://api.github.com/events'))
    tags.add(r.get(print_response, 'https://github.com/tsmanner/'))
    while len(tags) > 0:
        pass
