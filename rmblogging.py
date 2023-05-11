#!/bin/env python3
"""
RMB's logging module
"""

import argparse
import inspect
import sys
from datetime import datetime
from enum import IntEnum
from functools import partial


class LogLevels(IntEnum):
    """
    This class is an IntEnum on purpose: it allows log levels to be compared for <= and >=, which is
    very useful when deciding whether a message of a given log level should be printed based on the currently
    active log level.
    """
    EMERGENCY = 0    # system is unusable
    ALERT = 1        # action must be taken immediately
    CRITICAL = 2     # critical conditions
    ERROR = 3        # error conditions
    WARNING = 4      # warning conditions
    NOTICE = 5       # normal, but significant, condition
    INFO = 6         # informational message
    DEBUG = 7        # debug-level message


class Rmblogging:

    # Defaults for logging..
    loglevel = LogLevels.DEBUG
    MAX_COLUMNS = 190
    SHOW_CALLERNAME = False  # Whether to display the name of the calling function (at the far right end of the line)
    SHOW_MICROSECONDS = False  # Whether to display timestamps with microseconds precision.
    FIXED_LEVEL_LEN_ENABLED = True  # Whether to truncate the log level in the log line's prefix
    FIXED_LEVEL_LEN_LEN = 5
    print_func = print


def logmsg(level, msg):
    """
    Primitive to write a log message for various levels, using a well-defined format for each log line..

        [LEVEL TIMESTAMP] MESSAGE [CALLER]

    LEVEL     An attributes of LogLevels (e.g., LogLevels.LOG_INFO, LogLevels.LOG_ERR, etc.)
    TIMESTAMP Computed internally to be the current date/time at which this method is called.
    MESSAGE   The message passed in from the user, indirectly via one of the externally facing log methods.
    CALLER    The name of the user's method that called the externally facing log method. Note CALLER is
              displayed right-justified per the maximum number of columns configured in __init__.
              Disabled if SHOW_CALLERNAME is False.

    Parameters and return values..

    :param level: (LogLevels) Logging level
    :param msg: (str) The message to be displayed
    :return: (Nothing is returned)

    The following interal variables are used..

        level_str       (str)  The human-readable representation of the log level.
        msg_prefix      (str)  The "[LEVEL TIMESTAMP]" that starts each log line.
        msg_suffix      (str)  The "[CALLER]" displayed right-justified at the end of each log line.
        filler          (str)  A string of spaces used to push msg_suffix to its right-justified starting column.
        SHOW_CALLERNAME (bool) Set to False to disable displaying of the calling method at the RHS of the log message.
    """

    # Don't print messages if their loglevel isn't currently enabled..
    if level > Rmblogging.loglevel:
        return

    # Format the log line..

    level_str = level.name
    if Rmblogging.FIXED_LEVEL_LEN_ENABLED:
        format_specifier_a = "{:d}.{:d}s".format(Rmblogging.FIXED_LEVEL_LEN_LEN, Rmblogging.FIXED_LEVEL_LEN_LEN)
        format_specifier_b = "{:"+format_specifier_a+"}"
        level_str = format_specifier_b.format(level_str)

    now = datetime.now()
    myformatted_timestamp_now = f"{now.strftime('%Y-%m%d-%H%M%S')}"
    if Rmblogging.SHOW_MICROSECONDS:
        myformatted_timestamp_now += '.' + f'{now.microsecond:06d}'

    msg_prefix = f"[{level_str} {myformatted_timestamp_now}]"

    if Rmblogging.SHOW_CALLERNAME:
        msg_suffix = f"[{current_method_name()}]"
        filler = ' '*(Rmblogging.MAX_COLUMNS - len(msg_prefix) - len(msg_suffix) - len(msg) - 1)
        # Workaround for this module's current lack of support for multiline messages (msg_suffix was getting appended immediately adjacent to the output of the last line. Just skip the suffix if there's not enough room)
        if len(filler) <= 8:
            msg_suffix = ''
    else:
        filler = msg_suffix = ''

    # Print the log line..
    Rmblogging.print_func(f"{msg_prefix} {msg}{filler}{msg_suffix}")


def logmsg_and_raise_exception(level, msg):
    logmsg(level, msg)
    raise RuntimeError(msg)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Make each log severity into its own callable. User code is then only required to supply a single argument - the log message.
# Since the name of the callable impies its log severity, severity doesn't need to be passed in as another argument.
#
# Example..
#
# Instead of the user having to call..
#
#     logmsg_and_raise_exception(LogLevels.ERROR, 'Something went horribly wrong')
#
# ..the user code can call the much simpler and intuitive..
#
#     error('Something went horribly wrong')

emergency = partial(logmsg_and_raise_exception, LogLevels.EMERGENCY)
alert = partial(logmsg_and_raise_exception, LogLevels.ALERT)
critical = partial(logmsg_and_raise_exception, LogLevels.CRITICAL)
error = partial(logmsg_and_raise_exception, LogLevels.ERROR)
warning = partial(logmsg, LogLevels.WARNING)
notice = partial(logmsg, LogLevels.NOTICE)
info = partial(logmsg, LogLevels.INFO)
debug = partial(logmsg, LogLevels.DEBUG)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def current_method_name():
    """
    Inspects the calling stack, locating the name of the caller's caller. NOTE: Certain utility functions (e.g., logmsg(), info(),
    debug(), etc.) are ignored since 99.999% of the time we're truly interested in who called the utility, not the utility itself.

    :return: (str) The name of the calling function.
    """

    stack_iter = iter(inspect.stack())
    stack_iter.__next__()  # Eat the first one, it is this method, which we don't care about
    caller = stack_iter.__next__()

    # We also don't care about some utility methods ... we're really interested in the caller of those utility methods
    while caller.function in ['logmsg', 'debug', 'info', 'warning', 'error']:
        try:
            caller = stack_iter.__next__()
        except StopIteration:
            break
        # caller = frame[3]

    # I like to add a '()' to the end of the method name
    return f"{caller.function}()"


# ~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# * * *  APP DEMO  * * * |
# ~~~~~~~~~~~~~~~~~~~~~~~+

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Add to your app..
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#     import rmblogging
#     from rmblogging import Rmblogging, LogLevels, debug, info, notice, warning, error
#     
#     class YourAppDemo:
#     
#         def __init__(self, **kwargs):
#     
#             # Only if you want to allow setting log level from command line, put this in your app's __init__() ...
#     
#             parser = argparse.ArgumentParser()
#             parser.add_argument("--loglevel", default=None, type=str.upper, choices=['EMERGENCY', 'CRITICAL', 'ALERT', 'ERROR', 'WARNING', 'NOTICE', 'INFO', 'DEBUG'])
#             cmdline_args, unknown_args = parser.parse_known_args(sys.argv[1:])
#             if cmdline_args.loglevel is not None:
#                 Rmblogging.loglevel = LogLevels[cmdline_args.loglevel]
#
#             # Or, to manually override from inside this code, you only need to do this..
#
#             Rmblogging.loglevel = LogLevels.DEBUG
#     
#         def run(self):
#     
#             # Now you're ready to use logging..
#     
#             debug("debug, debug, debug, etc.")
#             info("ho hum, just some info")
#             notice("this is a notification only.")
#             warning("Whoa!! 'tis a warning!\n")
#     
#     
#     if __name__ == '__main__':
#     
#         Rmblogging.loglevel = LogLevels.DEBUG  # <- optional
#         app = YourAppDemo()
#         app.run()
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Or, for a simple, non-object based script..
#
#     import rmblogging
#     from rmblogging import Rmblogging, LogLevels, debug, info, notice, warning, error
#     
#     def doit():
#         debug('IN:  doit()')
#         debug('OUT: doit()')
#     
#     if __name__ == '__main__':
#         Rmblogging.loglevel = LogLevels.DEBUG  # optional, default is DEBUG (see top of class definition to confirm default hasn't changed)
#         Rmblogging.SHOW_MICROSECONDS = True    # optional, default is False (see top of class definition to confirm default hasn't changed)
#         Rmblogging.SHOW_CALLERNAME = True      # optional, default is False (see top of class definition to confirm default hasn't changed)
#         info('calling doit..')
#     
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

