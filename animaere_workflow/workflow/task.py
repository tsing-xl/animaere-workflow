# task.py from Animaere-workflow for python.
# Date: 26.03.28
# Version: 0

# Typing check
from typing import Callable, Any

# To compatible python 3.19 and lower, we import Union object instead of Type | Type.
from typing import Union

from uuid import uuid4, UUID
from ..exceptions import InvaildTaskOrSchedule
from ..handler import handler
from ..logging.log4a import logout
from ..consts import *

class Task:
    def __init__(
            self, 
            task_name: str, 
            task: str | Callable | None = None, 
            warning_level: str = EXCEPTION_THROW_DIRECTLY, # throw-directly or just-notify
            **task_config,
            ) -> None:
        '''A task is used to executing functions, or calling programs from outer.'''

        # The task of the whole Task object. could be a Callable object, a schedule, even outer programs.
        self.task = task

        self.task_index: int = -1

        # the warning level when Task is trying to raise a error.
        # The just-notify level will just throw the errors into screens and prints them out.
        self.warning_level = warning_level

        # Uuid of the task. Each task has its own uuid.
        self.task_uuid: Union[str, UUID] = uuid4()

        # The name of the task. For Task-index.
        self.task_name: str = str(task_name)

        # TODO: Add optional params
        self.task_optional: Any = task_config.get('optional', 'optional')

        # Task settings & function hooks.
        self.set_action_after_fail: Union[Task, Callable, None] = task_config.get('set_action_after_fail', None)
        
        # If successed, what should Task do next before running next Task. A hook for Task.
        self.set_action_after_success: Union[Task, Callable, None] = task_config.get('set_action_after_success', None)

        # If more fail caught, just throw them to after-more-fail.
        self.set_action_after_more_fail: Union[Task, Callable, None] = task_config.get('set_action_after_more_fail', None)
        
        # *Deprecated* self.action_before_execute: Task | Callable | None = task_config.get('action_before_execute', None)
        # The handler when task got a fatal error. Default to handler.default_error_handler.
        self.set_action_error_handler: Union[Callable, None] = task_config.get('set_action_error_handler', None)

        # Skip control, by returning a true or false.
        self.task_skip_control: Union[bool, Callable, None] = task_config.get('task_skip_control', None)
        
        # Check depencies before execute. The depencies could be a library, a schedule, few tasks, even a function.
        self.task_depencies: Union[list, tuple, Task, Callable, None] = task_config.get('task_depencies', [])

        # The task's metadata & infomations.

        # These are the counters for the Task. We count them, and storage them in here.
        self.task_execute_counter: int = 0
        self.task_success_counter: int = 0
        self.task_fail_counter: int = 0
        # ~self.task_failure_counter
        
        # the version of the task. An be displayed in int, str and interable object.
        self.task_version: Union[int, str, tuple, list, None] = 1

        # Description.
        self.task_description: Union[str, None] = None

        # Check if task was none.
        if self.task is None:
            if self.warning_level == EXCEPTION_JUST_NOTIFY:
                
                # Notiy the error in console/tty.
                logout('workflow.task', 3, 'An invaild task was created and the param task has been set to None. Nothing will happens because task did\'t know what to execute.')

            else:
                # Throw exception directly and halt the program.
                raise InvaildTaskOrSchedule('No task was setted or None was passed incorrectly')

        # Task type
        self.task_type: Union[str, ] = task_config.get('task_type', TYPE_ANY)
    
    def initialize_task(self) -> None:
        '''Used to initialize the task, to be sure there's no NoneType object contains. All value will be set to default.'''

        # Generate Uuids, and task name.
        if self.task_uuid is None: self.task_uuid: Union[str, UUID] = uuid4()
        if self.task_name is None: self.task_name: str = f'task-{self.task_name}'

        # If none, replace them to default values.
        if self.set_action_after_fail is None: self.set_action_after_fail = handler.Handler.fail_action_handler
        if self.set_action_after_success is None: self.set_action_after_success = handler.Handler.success_action_handler
        if self.set_action_after_more_fail is None: self.set_action_after_more_fail


class ExternalProgram:
    def __init__(
            self, 
            program_name: str | None = None, 
            path: str | None = None, 
            params: list = [], 
            ):
        'An module used to execute outer programs by subprocessing.'

        self.name = program_name
        self.path = path
        self.params = params
