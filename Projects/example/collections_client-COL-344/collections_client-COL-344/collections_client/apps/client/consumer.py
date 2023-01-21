from uplink import Consumer


class BaseConsumer(Consumer):
    base_url = ""
    auth = None

    def __init__(self, **kwargs):
        kwargs.setdefault("base_url", self.base_url)
        kwargs.setdefault("auth", self.auth)
        super().__init__(**kwargs)
