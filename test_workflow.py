from animaere_workflow import workflow

def test_workflow(*kw) -> None:
    print(' *** Testing with workflow by default...')
    _wf = workflow.Workflow()

def test_task(*kw) -> None:
    print(' *** Testing with task...')
    _tk = workflow.Task('default-task-name', warning_level = EXCEPTION_JUST_NOTIFY)
