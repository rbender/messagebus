import threading

class SerialBuffer:
    """ Simple wrapper around a Serial connection to add a non-blocking readline method """

    def __init__(self, connection):
        self._connection = connection
        self._buffer = ""
        self._lock = threading.Lock()

    def readline(self):
        if not self._lock.acquire(False):
            return None
        try:
            content = self._connection.read(self._connection.inWaiting() or 1)
            self._buffer += content

            if "\n" in content:
                line, self._buffer = self._buffer.split('\n', 1)
                return line
            else:
                return None
        finally:
            self._lock.release()