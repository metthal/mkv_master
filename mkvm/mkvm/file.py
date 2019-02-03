import tempfile
import os


class File:
    def __init__(self, path, handle=None):
        self.path = path
        self._handle = handle

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        if self._handle is not None:
            self._handle.close()
            self._handle = None

    @classmethod
    def temp(cls, ext=None):
        suffix = ('.' + ext) if ext else None
        tmp_file = tempfile.NamedTemporaryFile(prefix=os.getcwd() + os.path.sep, suffix=suffix)
        return cls(tmp_file.name, handle=tmp_file)

    @classmethod
    def none(cls):
        return cls(None)
