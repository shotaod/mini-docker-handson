import os
from typing import List

import linux


def child_proc_callback(option: dict):
    command = option['commands']
    os.execvp(command[0], command)


def exec_run(commands: List[str]):
    flags = 0
    option = {'commands': commands}
    pid = linux.clone(child_proc_callback, flags, (option,))

    os.waitpid(pid, 0)
