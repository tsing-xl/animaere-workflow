from .__init__ import Workflow, Task, consts

def test_workflow(*kw) -> None:
    print(' *** Testing with workflow by default...')
    _wf = Workflow()

def test_task(*kw) -> None:
    print(' *** Testing with task...')
    _tk = Task(warning_level = consts.EXCEPTION_JUST_NOTIFY)