# exceptions.py from Animaere-workflow for python.
# Date: 26.03.26
# Version: 1

class InvaildTaskOrSchedule(BaseException):
    '''An exception used to throw when user / program trying to create a invaild task or schedule.'''

class InvaildWorkflow(BaseException): 
    '''An exception used to throw when user / program trying to create a invaild workflow.'''

class FailedToExecuteTaskOrSchedule(BaseException):
    '''Throws when a task/schedule execute incorrectly.'''