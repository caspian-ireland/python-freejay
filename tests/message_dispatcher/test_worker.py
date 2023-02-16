import pytest
import queue
import threading
import retry
from freejay.message_dispatcher import worker
from freejay.messages import messages as mes


@pytest.fixture
def handler_f():
    class Handler:
        def __init__(self):
            self.count = 0
            self.lock = threading.Lock()

        def __call__(self, message: mes.Message) -> None:
            with self.lock:
                self.count += 1

    return Handler()


@pytest.fixture
def msg():
    msg = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_VIEW, trigger=mes.Trigger.BUTTON),
        content=mes.Button(
            press_release=mes.PressRelease.PRESS,
            component=mes.Component.LEFT_DECK,
            element=mes.Element.CUE,
        ),
        type=mes.Type.KEY,
    )
    return msg


@retry.retry(tries=5, delay=0.1)
def assert_returns_true_false(func, expected=True):
    if expected:
        assert func()
    else:
        assert not func()


@pytest.mark.slow
def test_workcycle_stopped(handler_f):

    q = queue.Queue()
    t_workcycle = worker.WorkCycle(q, handler_f)
    t = threading.Thread(target=t_workcycle.start, daemon=True)
    t.start()
    assert_returns_true_false(t.is_alive, True)
    t_workcycle.running = False
    assert_returns_true_false(t.is_alive, False)


@pytest.mark.slow
def test_workcycle_running(handler_f, msg):

    q = queue.Queue()
    t_workcycle = worker.WorkCycle(q, handler_f)
    t = threading.Thread(target=t_workcycle.start, daemon=True)
    t.start()
    q.put(msg)
    q.put(msg)
    q.put(msg)
    assert_returns_true_false(lambda: handler_f.count == 3, True)
    t_workcycle.running = False


@pytest.mark.slow
def test_worker_start(handler_f):

    q = queue.Queue()
    t_workcycle = worker.WorkCycle(q, handler_f)
    t_worker = worker.Worker(t_workcycle, thread_count=1)
    t_worker.start()
    assert_returns_true_false(t_worker.thread[0].is_alive, True)


@pytest.mark.slow
def test_worker_stop(handler_f):

    q = queue.Queue()
    t_workcycle = worker.WorkCycle(q, handler_f)
    t_worker = worker.Worker(t_workcycle)
    t_worker.start()
    assert_returns_true_false(t_worker.thread[0].is_alive, True)
    t_worker.stop()
    assert_returns_true_false(t_worker.thread[0].is_alive, False)


@pytest.mark.slow
def test_worker_running(handler_f, msg):

    q = queue.Queue()
    t_workcycle = worker.WorkCycle(q, handler_f)
    t_worker = worker.Worker(t_workcycle)
    t_worker.start()

    q.put(msg)
    q.put(msg)
    q.put(msg)
    assert_returns_true_false(lambda: handler_f.count == 3, True)
    t_worker.stop()


@pytest.mark.slow
def test_worker_start_multi_thread(handler_f):

    thread_count = 3
    q = queue.Queue()
    t_workcycle = worker.WorkCycle(q, handler_f)
    t_worker = worker.Worker(t_workcycle, thread_count=thread_count)
    t_worker.start()
    for i in range(thread_count):
        assert_returns_true_false(t_worker.thread[i].is_alive, True)


@pytest.mark.slow
def test_worker_stop_multi_thread(handler_f):

    thread_count = 3
    q = queue.Queue()
    t_workcycle = worker.WorkCycle(q, handler_f)
    t_worker = worker.Worker(t_workcycle, thread_count=thread_count)
    t_worker.start()
    for i in range(thread_count):
        assert_returns_true_false(t_worker.thread[i].is_alive, True)

    t_worker.stop()
    for i in range(thread_count):
        assert_returns_true_false(t_worker.thread[i].is_alive, False)


@pytest.mark.slow
def test_worker_running_multi_thread(handler_f, msg):

    thread_count = 3
    q = queue.Queue()
    t_workcycle = worker.WorkCycle(q, handler_f)
    t_worker = worker.Worker(t_workcycle, thread_count=thread_count)
    t_worker.start()

    q.put(msg)
    q.put(msg)
    q.put(msg)

    assert_returns_true_false(lambda: handler_f.count == 3, True)
    t_worker.stop()
