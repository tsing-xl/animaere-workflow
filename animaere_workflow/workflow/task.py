# task.py from Animaere-workflow for python.
# Date: 26.03.28
# Version: 0

# Typing check
from typing import Callable, Any

# To compatible python 3.9 and lower, we import Union object instead of Type | Type.
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
            task: Union[str, Callable, None] = None, 
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
        
        # Check dependencies before execute. The dependencies could be a library, a schedule, few tasks, even a function.
        self.task_dependencies: Union[list, tuple, Task, Callable, None] = task_config.get('task_dependencies', [])

        # print(self.task_dependencies)

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
        
        # The state of Task.
        self.is_running: bool = False
        self.task_done: bool = False

        # Check if task was none.
        if self.task is None:
            if self.warning_level == EXCEPTION_JUST_NOTIFY:
                
                # Notiy the error in console/tty.
                logout('workflow.task', 3, 'An invaild task was created and the param task has been set to None. Nothing will happens because task did\'t know what to execute.')

            else:
                # Throw exception directly and halt the program.
                raise InvaildTaskOrSchedule('No task was setted or None was passed incorrectly')
        
        # Check task's type automatically.
        if isinstance(self.task, Callable): self.task_type: str = TYPE_LOCAL_FUNCTION

        elif isinstance(self.task, Task): self.task_type: str = TYPE_TASK

        elif isinstance(self.task, ExternalProgram): self.task_type: str = TYPE_EXTERNAL_PROGRAM

        else:
            # User can also complete the type of task. But more convient is throw a known object instead of strings.
            if task_type := task_config.get('task_type', None):
                self.task_type = task_type
            
            # User did't gave the param task_type. Switch the type to TYPE_ANY.
            else:
                self.task_type: str = TYPE_ANY

        # Type schedule
        # elif isinstance(self.task, )

        # Task type [Deprecated]
        # self.task_type: Union[str, ] = task_config.get('task_type', TYPE_ANY)

        # You don't need to call initialize_task manually. The Task will help you to do this.
        self.initialize_task()
    
    def initialize_task(self) -> None:
        '''Used to initialize the task, to be sure there's no NoneType object contains. All value will be set to default.'''

        # Generate Uuids, and task name.
        if self.task_uuid is None: self.task_uuid: Union[str, UUID] = uuid4()
        if self.task_name is None: self.task_name: str = f'task-{self.task_name}'

        # If none, replace them to default values.
        if self.set_action_after_fail is None: 
            self.set_action_after_fail: Callable = handler.Handler.fail_action_handler
        
        # If none, replace it to default success handler.
        if self.set_action_after_success is None: 
            self.set_action_after_success: Callable = handler.Handler.success_action_handler
        
        if self.set_action_after_more_fail is None: 
            self.set_action_after_more_fail: Callable = handler.Handler.more_fail_action_handler
        
        if self.set_action_error_handler is None: 
            self.set_action_error_handler: Callable = handler.Handler.error_handler
        
        # After doing these, notify user.
        logout('workflow.task', 0, f'Task {self.task_name} was alreay initialized.')

        # For debugging
        # logout('workflow.task (debug)', 1, f'Task: {self.task}, Task name: {self.task_name}, Task uuid: {self.task_uuid}')
    
    def run(self, ) -> bool:
        '''
        Execute the Task and check the dependencies before running.
        
        Also, you can just execute the Task direstly. 
        Bue we don't recommend this way beacuse of the task dependencies and state check.
        
        Returns True if Task executed successfully. Otherwise return False.'''
        # Check the state if task is already executed.
        if self.task_done: return True

        # The whole process of executing Task.
        # Firstly, check if task is available.
        if self.task_type == TYPE_ANY:
            
            # WONTFIX: Allow user execute a task by gave a special string.
            return False
        
        # Set the state of Task to 'running'.
        self.is_running: bool = True

        # Next, check dependencies before run.
        if self.check_dependencies():

            # Only passed check_dependencies, the task will continue.
            try:
                if isinstance(self.task, Callable): self.task()

                if isinstance(self.task, Task): self.task.run()
            except Exception as errors:

                # If an error has been caught, throw it to error_handler.
                self.set_action_after_fail(
                    self.task_name, 
                    errors, 
                )

                self.task_fail_counter += 1
                
                # Return a false to let users and program know.
                return False
            
            else:
                self.task_success_counter += 1

                # After running task, execute the success hook first.
                self.set_action_after_success(
                    self.task_name, 
                    'Task has been executed successfully', 
                )

                # Set the done make to True.
                self.task_done: bool = True

            finally: 
                # Set the running state to False.
                self.is_running: bool = False

                self.task_execute_counter += 1

        else:

            # Throw it to fail_handler.
            self.set_action_after_fail(
                self.task_name, 
                'Failed to resolve dependencies', 
            )
    
    def check_dependencies(self, ) -> bool:
        '''Check the dependencies of the Task. 
        
        If success, return True, otherwise return False.'''
        if self.task_dependencies is None or self.task_dependencies == []:
            
            # No dependencies exist. just skip
            logout(f'workflow.task {self.task_name}', 0, 'No dependencies found. Skipping...')
            return True

        # Execute them, and make sure they are already done.
        for task_index in self.task_dependencies:
            
            # Skip string dependencies.
            # if isinstance(task_index, str): continue
            if isinstance(task_index, Task):

                # Check uuid and Task name if loop calling.
                if task_index.task_uuid == self.task_uuid or task_index.task_name == self.task_name:
                    
                    # Found loop calling. Return 'fail' status.
                    logout(f'workflow.task {self.task_uuid}', 2, 'A loop calling was detected by check_dependencies. Check your workflow or Task dependencies before running!')
                    return False 
                
                # Otherwise, just run. What problem cound be?
                task_index.run()

            elif isinstance(task_index, Callable):

                # Attention: return 'false' will raise a 'fail' status in check_dependencies.
                try:
                    _task_state = task_index()
                
                except Exception as error:
                    
                    # Catched error, print them out and return a 'fail' status.
                    logout(f'workflow.task {self.task_uuid}', 3, f'Failed to execute dependencies {task_index}: {error}')
                    return False

                else: 
                    # If Nothing happens, check the state.
                    if not _task_state: # Note: not True -> False

                        logout(f'workflow.task {self.task_uuid}', 3, f'Dependencies failed: {task_index}.')
                        return False

                    # Yeah, nothing happens, let's just returns a true to let them know we are 'success'.
            
            # ...
        logout(f'workflow.task {self.task_name}', 0, 'All dependencies are resolved.')
        return True
        
class LightWeightedTask: None

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