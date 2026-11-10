"""Stop after real native execution returns, before campaign completion commits."""

import os
from pathlib import Path
import runpy
import sys

runner = Path(sys.argv[1]).resolve()
role = sys.argv[2]
sys.argv = [str(runner), *sys.argv[3:]]


def stop(frame, event, arg):
    if (event == 'line' and Path(frame.f_code.co_filename).resolve() == runner
            and frame.f_code.co_name == 'execute_attempt' and 'summary' in frame.f_locals
            and frame.f_locals['attempt']['role'] == role):
        os._exit(99)
    return stop


sys.settrace(stop)
runpy.run_path(str(runner), run_name='__main__')
