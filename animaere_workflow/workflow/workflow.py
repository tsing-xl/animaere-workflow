# workflow.py from Animaere-workflow for python.
# Date: 26.03.26
# Version: 0

from typing import Callable, Union
from uuid import uuid4
from ..logging.log4a import logout
from ..handler.handler import *

class Workflow:
    def __init__(
            self, 
            workflow_name: str | None = None,  
            ) -> None:
        '''
        A workflow is used to process things in order.

        Beside the basic workflow, we also contains a lot of new features. Such as:
        
        * automatic - Create workflow files automatically and executing them without dealing with troubles manually.
        * logging - We records the behavior of tasks & workflows, so it's easy to resolve problems.
        * link-to - You can link to other programs by subprocess or network calling.

        The workflow grammar like: 
        (Symbols like $, # to perfomance status) from_module.function: arg1, arg2, arg3, ...
        '''

        # Basic settings of workflow.
        self.workflow_name: str = workflow_name
        self.workflows: Union[list, tuple] = []
        self.token: str = '_token'
        
        # If false, any changes of workflow will strictly rejected.
        self._read_only: bool = False

    def create_new_task(self, task_name: Union[Callable, ], task_index: int = -1) -> bool:
        '''Create a new task in your workflow.'''

        # if task name is a callable object.
        # TODO: Add more kinds of task.
        
        # lf Means this is a local function.
        if isinstance(task_name, Callable): task_name = '~lf@' + str(task_name)
        elif isinstance(task_name, str): task_name = '~any@' + str(task_name)

        # TODO: Add safety protection in future version. (security-fix)

        # Debug
        # logout('workflow.workflow', 0, f'Task: {task}')

        # Warnings if using an [any] workflow.
        # if task['task-name'].startswith('~any@'): logout('workflow.workflow', 2, 'Try functions or workflow.Task instead of an [any] workflow.')

        # Append the task into workflow.
        # self.workflows.append(task)

    @property
    def read_only(self) -> bool: return self._read_only

    # For safety, only authorized users / programs can modify some value.
    @read_only.setter
    def read_only(self, value: any) -> None: return