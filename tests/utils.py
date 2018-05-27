import sys
from contextlib import contextmanager
from io import StringIO


@contextmanager
def capture_output():
    """
    Temporarily capture stdout/stderr streams.
    """
    tmpout, tmperr = StringIO(), StringIO()
    stdout, stderr = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = tmpout, tmperr
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = stdout, stderr
