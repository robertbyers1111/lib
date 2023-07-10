#!/bin/env python
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
rmbimage.py - My image library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import PIL as Image  # <-- for future use
import subprocess as sp
import rmblogging
from rmblogging import debug, error

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def run_gegl(gegl_params):
"""
Invoke the external gegl CLI process using the command line passed in from caller
"""

    gegl_full_command = ['gegl'] + gegl_params

    debug('')
    debug(f'Running gegl cli..')
    debug(f'{gegl_full_command = }')

    # Run the gegl command..

    try:
        completed_process = sp.run(gegl_full_command, timeout=300, check=True, capture_output=True, encoding="utf-8")

    except FileNotFoundError as e:
        error(f"Process failed because the executable could not be found.\n{e}")

    except sp.CalledProcessError as e:
        error(f"Process failed because did not return a successful return code. Returned {e.returncode}\n{e}")

    except sp.TimeoutExpired as e:
        error(f"Process timed out.\n{e}")

    debug(f"{completed_process = }")

    for line in completed_process.stdout:
        debug(f"{line[:188] = }")

