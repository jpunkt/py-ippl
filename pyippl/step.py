import logging
import functools

from enum import Enum
from typing import Callable
from .ex import StopProcessingException, ExecutionError

"""
Framework for image processing pipeline
"""


logger = logging.getLogger(__name__)


class ProcessStep:
    """
    Decorator for an (image processing) function.
    The decorated function must return a `ProcessReturn` object or raise a
    `StopProcessingException` and can be assigned up to three exit functions,
    as follows:

    - do_next:  called when processing step was completed normally
    - noop:     called when this processing step yielded no result, but did not
                raise an exception
    - on_error: called when processing step raised an exception

    Calling the decorated function raised any exception, this Decorator returns
    `False`, otherwise `True`.

    If no exit function is defined, the pipe ends, but returns `True`

    """
    def __init__(self, func: Callable):
        functools.update_wrapper(self, func)
        self.func = func

        self.noop: 'ProcessStep' = None        # Exit Event
        self.do_next: 'ProcessStep' = None     # Exit and continue with
                                               # next processing step
        self.on_error: Callable = None         # Exit with an error state

    def __call__(self, *args, **kwargs):
        """
        Process stuff
        """
        ret = None
        try:
            logger.debug(f'Running {self.func}')
            ret = self.func(*args, **kwargs)
        except StopProcessingException as s:
            logger.info(f'End of pipe reached.')
            return False
        except KeyError as ke:
            # Some Step didn't get the required keys
            logger.warning(f'Function {self.func} raised {ke}')
            # Do not escalate, treat as NOOP
            if self.noop is not None:
                self.noop(*args, **kwargs)
        except Exception as e:
            if self.on_error is not None:
                self.on_error(e)
            else:
                raise e

        if (ret is ProcessReturn.NEXT) and (self.do_next is not None):
            return self.do_next(*args, **kwargs)
        elif (ret is ProcessReturn.NOOP) and (self.noop is not None):
            return self.noop(*args, **kwargs)
        else:
            return True


class ProcessReturn(Enum):
    NOOP = 0
    NEXT = 1


