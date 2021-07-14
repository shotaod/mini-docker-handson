import os
from typing import List

import linux

import commands.cgroup as cgroup


def child_proc_callback(option: dict):
    pid = os.getpid()
    print(f'pid: {pid}')

    cg = cgroup.CGroup('hogehoge')
    cg.set_cpu_limit(.25)
    cg.add(pid)

    command = option['commands']
    os.execvp(command[0], command)


def exec_run(commands: List[str]):
    flags = 0
    option = {'commands': commands}
    pid = linux.clone(child_proc_callback, flags, (option,))

    os.waitpid(pid, 0)
