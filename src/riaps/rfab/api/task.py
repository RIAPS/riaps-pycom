'''
- Some tasks will have a step that requires output from a prior step
'''

class step:
    '''Single command
    Customizeable pass/fail test
    Accepts kwargs for Connection command?
    Leaf instances are in a specific _conntext
    '''
    pass

class _conntext:
    '''A single Connection object's context, instances of steps
    '''
    pass


class Task(dict):
    '''Base class for Rfab tasks, executes N steps for M connections
    All M connections must be able to execute all N steps. If more complicated
    patterns are needed, use multiple Tasks.
    - Multi-threaded: yes/no
        - If multithreaded, lock-step yes/no
    - Stop on problem or keep going
    '''
    def __init__(self,
        connections,
        **kwargs,
    ):
        self.connections = connections
        for c in self.connections:
            self[c] = _conntext()


    def run(self):
        pass
        # If lock-step, start&join threads for each step
        # if not lock-step, dispatch all steps to thread? 
        # If RR/single, repeat lock-step for each conn in loop?

    def _run_parallel(self):
        pass

    def _run_serial(self):
        pass