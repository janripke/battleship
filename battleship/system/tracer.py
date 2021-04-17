import sys


def build():
    code, message, backtrace = sys.exc_info()

    # not sure if we need this, used backtrace variable instead
    # format_backtrace = "".join(traceback.format_exception(code, message, backtrace))

    result = {
        'code': repr(code),
        'message': repr(message),
        'backtrace': repr(backtrace)
    }

    return result
