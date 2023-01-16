import queue
from freejay import messages as mes


# credit https://maldus512.medium.com/how-to-setup-correctly-an-application-with-python-and-tkinter-107c6bc5a45


def worker(player, q):
    message: mes.Message = None
    while True:
        try:
            message = q.get(timeout=0.1)

            if message.content. == events.Action.PlayPause:
                if event.payload.press_release == events.PressRelease.Press:
                    player.play_pause()
            if event.payload.action == events.Action.Cue:
                if event.payload.press_release == events.PressRelease.Press:
                    player.cue_press()
                elif event.payload.press_release == events.PressRelease.Release:
                    player.cue_release()

        except queue.Empty:
            pass



