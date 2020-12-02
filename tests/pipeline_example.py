from pyippl import ProcessStep, ProcessReturn, StopProcessingException


class TestContext:
    def __init__(self,
                 inc=1,
                 inc_initial=0,
                 terminate_condition=5):
        self.inc = inc
        self.inc_initial = inc_initial
        self.terminate_condition = terminate_condition


@ProcessStep
def test1(context, transport):
    print('Executing test1')
    return ProcessReturn.NEXT


@ProcessStep
def increment(context, transport):
    inc = transport['inc'] = transport.get('inc',
                                           context.inc_initial) + context.inc
    print(f'Incrementing. Counter={inc}')
    return ProcessReturn.NEXT


@ProcessStep
def condition(context, transport):
    if transport['inc'] > context.terminate_condition:
        print('Stop execution.')
        raise StopProcessingException
    return ProcessReturn.NOOP


@ProcessStep
def noop(context, transport):
    print("noop.")


if __name__ == '__main__':
    ctxt = TestContext()
    trans = {}

    test1.do_next = increment
    increment.do_next = condition
    condition.noop = noop

    while test1(ctxt, trans):
        pass
