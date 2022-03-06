import linux
import os
from typing import List
import commands.cgroup as cgroup

def child_proc_callback(option: dict):
    pid = os.getpid()
    print(f"container pid: {pid}")
    
    linux.sethostname("container")
    
    cpu = option['cpu']
    if cpu:
    	cg = cgroup.CGroup('container')
    	cg.set_cpu_limit(cpu)
    	cg.add(pid)

    command = option['command']
    os.execvp(command[0], command)


def exec_run(cpu: float, command: List[str]):
    flags = (linux.CLONE_NEWUTS | # UTS名前空間
    	linux.CLONE_NEWPID # PID名前空間
    )
    option = {'cpu': cpu, 'command': command}
    child_pid = linux.clone(
        child_proc_callback,
        flags,
        (option, )
    )

    os.waitpid(child_pid, 0)

