# handler.py from Animaere-workflow for python.
# Date: 26.03.26
# Version: 0

from typing import Callable, Union, Any
from ..logging.log4a import logout
from ..exceptions import *
from ..consts import *

# STD Handler

class Handler:
    def error_handler(
            task_name_or_uuid: Union[str, None] = None, 
            error: Union[str, BaseException, None] = None, 
            error_description: Union[str, None] = None, 
            level: Union[str, None] = EXCEPTION_JUST_NOTIFY, 
        ) -> None:
        '''A standard handler used to handle errors that tasks threw.'''

        # If EXCEPTION_JUST_NOTIFY and None, just print a log on the screen.
        if level == EXCEPTION_JUST_NOTIFY or None:
            logout(f'task {task_name_or_uuid} -> handler.error_handler', 3, f'{error}: {error_description}')
        
        # Throw the error directly if error is a BaseException object.
        else:
            if isinstance(error, BaseException): raise error(error_description)

            # If not, raise FailedToExecuteTaskOrSchedule.
            raise FailedToExecuteTaskOrSchedule(f'Failed to execute task/schedule: {error}: {error_description}')

    def fail_action_handler(
            task_name_or_uuid: Union[str, None] = None, 
            fail_reason: Union[str, None] = None, 
            *kw: Any, 
    ) -> None:
        logout(f'task {task_name_or_uuid} -> handler.fail_action_handler', 3, f'Action failed: {fail_reason}')
    
    def success_action_handler(
            task_name_or_uuid: Union[str, None] = None, 
            success_reason: Union[str, None] = None, 
            *kw: Any, 
    ) -> None:
        logout(f'task {task_name_or_uuid} -> handler.success_action_handler', 0, f'Action successed: {success_reason}')
    
    def more_fail_action_handler(
            task_name_or_uuid: Union[str, None] = None, 
            fail_reason: Union[str, None] = None, 
            *kw: Any, 
    ) -> None:
        logout(f'task {task_name_or_uuid} -> handler.more_fail_action_handler', 3, f'Action failed for more than once: {fail_reason}')

# Another way, the default exception/event handler.
default_error_handler: Callable = Handler.error_handler