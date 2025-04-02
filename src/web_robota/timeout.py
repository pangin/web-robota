import time
import signal

from .type import SimpleInstruction


def timeout(seconds_before_timeout: int = SimpleInstruction.timeout):
    def decorate(f):
        def handler(signum, frame):
            raise TimeoutError()

        def new_f(*args, **kwargs):
            old = signal.signal(signal.SIGALRM, handler)
            old_time_left = signal.alarm(int(seconds_before_timeout))

            if 0 < old_time_left < seconds_before_timeout:
                signal.alarm(old_time_left)

            start_time = time.time()

            try:
                result = f(*args, **kwargs)
            finally:
                if old_time_left > 0:
                    old_time_left -= time.time() - start_time

                signal.signal(signal.SIGALRM, old)
                signal.alarm(old_time_left)
            return result

        new_f.__name__ = f.__name__

        return new_f

    return decorate
