"""Protocols for Message Producers and Consumers.

Producers emit messages whilst Consumers recieve messages.
"""

from __future__ import annotations
import typing
import abc
from freejay import messages


class Producer(typing.Protocol):
    """Message Producer Protocol."""

    consumer: typing.Optional[Consumer]

    def register_consumer(self, consumer: Consumer):
        """Register a consumer. Generally not called directly.

        Args:
            consumer (Consumer): Anything that implements the Consumer protocol.
        """
        self.consumer = consumer

    def send_message(self, message: messages.Message):
        """Send message to consumer.

        Args:
            message (messages.Message): Message to send
        """
        self.consumer(message)


class Consumer(typing.Protocol):
    """Message Consumer Protocol."""

    def listen(self, producer: Producer):
        """Listen for messages from a Producer.

        Args:
            producer (Producer): Anything that implements the Producer protocol.
        """
        producer.register_consumer(self)

    @abc.abstractmethod
    def on_message_recieved(self, message: messages.Message):
        """Do something with a recieved message.

        This is an abstract method that must be overridden by the
        class implementing this protocol.

        Args:
            message (messages.Message): Message to process.
        """
        pass

    def __call__(self, message: messages.Message):
        """Call on_message_recieved() method.

        Args:
            message (messages.Message): Message to process.
        """
        return self.on_message_recieved(message)
