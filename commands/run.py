import linux
import os
from typing import List

def child_proc_callback(command: List[str]):
    print(f"container pid: {os.getpid()}")
    os.execvp(command[0], command)

def exec_run(command: List[str]):
    flags = 0
    child_pid = linux.clone(
        child_proc_callback,
        flags,
        (command, )
    )

    os.waitpid(child_pid, 0)

