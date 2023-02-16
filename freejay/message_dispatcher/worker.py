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


class WorkManager:
    """
    Manage multiple workers.

    Each worker is associated with a different queue and set of threads. This makes
    it possible to separate different types of tasks.
    """

    def __init__(self):
        """Construct WorkStreams object."""
        self.workers: typing.Dict[str, Worker] = dict()

    def add_worker(self, worker: Worker, name: str):
        """Add a worker.

        Args:
            worker (Worker): Worker to add.
            name (str): Worker name
        """
        self.workers[name] = worker

    def start(self):
        """Start the workers."""
        for name, worker in self.workers.items():
            worker.start()

    def stop(self):
        """Stop the workers."""
        for name, worker in self.workers.items():
            worker.stop()

    def put(self, item: typing.Any, worker_name: str):
        """Put an item in a worker queue.

        Args:
            item (typing.Any): Item to add to queue.
            worker_name (str): Name of worker.
        """
        self.workers[worker_name].workcycle.q.put(item)

    def pop(self, worker_name: str) -> typing.Any:
        """Get an item from a worker queue.

        Args:
            worker_name (str): Name of worker.
        """
        self.workers[worker_name].workcycle.q.get()

    def get_queue(self, worker_name: str) -> queue.Queue:
        """Get a worker queue.

        Args:
            worker_name (str): Name of worker.

        Returns:
            Queue: Worker Queue
        """
        return self.workers[worker_name].workcycle.q

    def get_handler(self, worker_name: str) -> typing.Callable[[mes.Message], None]:
        """Get a worker handler.

        Args:
            worker_name (str): Name of worker.

        Returns:
            typing.Callable[[mes.Message], None]: Message Handler
        """
        return self.workers[worker_name].workcycle.handler


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
