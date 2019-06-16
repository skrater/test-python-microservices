class Topic(object):
    _receivers = {}

    def __init__(self, topic_name):
        self._topic_name = topic_name

    def subscribe(self, receiver):
        if not callable(receiver):
            raise ValueError('Receiver must be callable.')

        self._receivers[self._topic_name] = receiver

    def publish(self, *args, **kwargs):
        receiver = self._receivers.get(self._topic_name, None)

        if not receiver:
            return True

        return receiver(*args, **kwargs)

    def unsubscribe(self, receiver):
        return self._receivers.pop(self._topic_name, None)

    @classmethod
    def clear(cls):
        cls._receivers = {}

    @classmethod
    def receivers(cls):
        return list(cls._receivers)


def subscribe(topic_name):
    def wrap(receiver):
        Topic(topic_name).subscribe(receiver)
        return receiver
    return wrap
