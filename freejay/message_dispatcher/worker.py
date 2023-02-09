"""
Worker pulls messages from the queue and passes to the message handler.
"""

import queue
import typing
import threading
from freejay.messages import messages as mes
from freejay.messages import produce_consume as prodcon


class WorkCycle:
    """Poll a queue for messages and pass them to a handler."""

    def __init__(
        self,
        q: queue.Queue[mes.Message],
        handler: typing.Callable[[mes.Message], None],
    ):
        """Construct WorkCycle.

        Args:
            q (queue.Queue[typing.Type[mes.Message]]): Message queue
            handler (typing.Callable[[mes.Message], None]): Message handler
        """
        self.q = q
        self.handler = handler
        self.running = False

    def start(self):
        """Start the workcycle."""
        self.running = True
        while True and self.running:
            try:
                message = self.q.get(timeout=0.1)
                self.handler(message)

            except queue.Empty:
                pass


class Worker:
    """Run a workcycle on one or more daemon threads."""

    def __init__(self, workcycle: WorkCycle, thread_count: int = 1):
        """Construct Worker.

        Args:
            workcycle (WorkCycle): Workcycle to run.
            thread_count (int): Number of threads to run worker on.
        """
        self.workcycle = workcycle
        self.thread_count = thread_count
        self.thread: typing.List = list()

    # TODO - Do I need to worry about thread leakage here?
    def start(self):
        """Start the workcycle."""
        for i in range(self.thread_count):
            thread = threading.Thread(target=self.workcycle.start, daemon=True)
            self.thread.append(thread)
            thread.start()

    def stop(self):
        """Stop the workcycle."""
        self.workcycle.running = False


class QueueListener(queue.Queue, prodcon.Consumer):
    """
    Queue Listener.

    Extends the Queue class, implementing the Consumer protocol
    to add messages to the queue when messages are received.
    """

    def on_message_recieved(self, message: mes.Message):
        """
        Recieve Messages.

        When messages are recieved, they are added to the queue.

        Args:
            message (mes.Message): Message
        """
        self.put(message)
