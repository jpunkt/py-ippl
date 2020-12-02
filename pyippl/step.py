import logging
import functools

from enum import Enum
from typing import Callable
from .ex import StopProcessingException

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

        self.__noop: 'ProcessStep' = None       # Exit Event
        self.__do_next: 'ProcessStep' = None    # Exit and continue with
                                                # next processing step
        self.__on_error: 'ProcessStep' = None   # Exit with an error state

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
        except Exception as e:
            logger.warning(f'Function {self.func} raised1 {e}')
            #
            if self.on_error is not None:
                return self.on_error(e, *args, **kwargs)
            else:
                raise e

        if (ret is ProcessReturn.NEXT) and (self.do_next is not None):
            return self.do_next(*args, **kwargs)
        elif (ret is ProcessReturn.NOOP) and (self.noop is not None):
            return self.noop(*args, **kwargs)
        else:
            return True

    @property
    def noop(self):
        return self.__noop

    @noop.setter
    def noop(self, noop: 'ProcessStep'):
        if (noop is not None) and (type(noop) is not ProcessStep):
            raise TypeError(f'Functions passed as noop must be of type '
                            f'ProcessStep (got {type(noop)})')
        self.__noop = noop

    @property
    def do_next(self):
        return self.__do_next

    @do_next.setter
    def do_next(self, do_next: 'ProcessStep'):
        if (do_next is not None) and (type(do_next) is not ProcessStep):
            raise TypeError(f'Functions passed as noop must be of type '
                            f'ProcessStep (got {type(do_next)})')
        self.__do_next = do_next

    @property
    def on_error(self):
        return self.__on_error

    @on_error.setter
    def on_error(self, on_error: Callable):
        if (on_error is not None) and not callable(on_error):
            raise TypeError(f'Functions passed as noop must be of type '
                            f'Callable (got {type(on_error)})')
        self.__on_error = on_error


class ProcessReturn(Enum):
    NOOP = 0
    NEXT = 1
