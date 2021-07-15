import os
from typing import List

import linux

import commands.local as local
import commands.cgroup as cgroup


def child_proc_callback(option: dict):
    pid = os.getpid()
    print(f'pid: {pid}')

    cpu = option['cpu']
    if cpu:
        cg = cgroup.CGroup('hogehoge')
        cg.set_cpu_limit(cpu)
        cg.add(pid)

    linux.sethostname('container-process')

    command = option['commands']
    os.execvp(command[0], command)


def exec_run(cpu: float, commands: List[str]):

    image = next((v for v in local.find_images() if v.name == 'library/busybox'), None)
    print(f'found busybox image : {image}')

    flags = linux.CLONE_NEWUTS
    option = {'cpu': cpu, 'commands': commands}
    pid = linux.clone(child_proc_callback, flags, (option,))

    os.waitpid(pid, 0)
