import queue
import typing
from freejay import handler
from freejay import messages as mes


# credit https://maldus512.medium.com/how-to-setup-correctly-an-application-with-python-and-tkinter-107c6bc5a45


class Worker:
    def init(self, q: queue.Queue[typing.Type[mes.Message]], handler: handler.Handler):
        self.q = q
        self.handler = handler

    def process(self):
        while True:
            try:
                message = self.q.get(timeout=0.1)
                self.handler(message)

            except queue.Empty:
                pass


### Manual Testing ###


# class ExampleClass:
#     def __init__(self):
#         self.a = "Something Cool"

#     def somemethod(self):
#         print(self.a)


# msg = mes.Message(
#     sender=mes.Sender(source=mes.Source.PLAYER, trigger=mes.Trigger.BUTTON_PRESS),
#     content=mes.Button(
#         press_release=mes.PressRelease.PRESS,
#         component=mes.Component.LEFT_DECK,
#         element=mes.Element.CUE,
#     ),
#     type=mes.Type.KEY,
# )


# myhandler = Handler()

# exampleclass = ExampleClass()
# button_cb = make_button_cb(exampleclass.somemethod)

# myhandler.register_handler(
#     callback=button_cb,
#     component=mes.Component.LEFT_DECK,
#     element=mes.Element.CUE,
# )

# myhandler(msg)
