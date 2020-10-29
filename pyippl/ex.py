class StopProcessingException(Exception):
    """
    This exception can be raised by a `ProcessStep` decorated function to end
    the processing pipeline.
    """
    pass


class ExecutionError(Exception):
    """
    This exception can be raised by a `ProcessStep` decorated function if
    execution is not possible
    """
    pass
