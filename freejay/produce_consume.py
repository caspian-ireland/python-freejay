from __future__ import annotations
import typing
import abc
from freejay import messages


class Producer(typing.Protocol):

    consumer: typing.Optional[Consumer]

    def register_consumer(self, consumer: Consumer):
        self.consumer = consumer

    def send_message(self, message: messages.Message):
        self.consumer(message)


class Consumer(typing.Protocol):
    def listen(self, producer: Producer):
        producer.register_consumer(self)

    @abc.abstractmethod
    def on_message_recieved(self, message: messages.Message):
        pass

    def __call__(self, message: messages.Message):
        return self.on_message_recieved(message)
