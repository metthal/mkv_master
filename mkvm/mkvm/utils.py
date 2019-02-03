import os
import tempfile


def tmp_file(suffix):
    return tempfile.NamedTemporaryFile(prefix=os.getcwd() + os.path.sep, suffix='.' + suffix)
