import os
from typing import List

import linux

import commands.cgroup as cgroup
import commands.data as data
import commands.format as fmt
import commands.local as local


def child_proc_callback(option: dict):
    pid = os.getpid()
    print(f'pid: {pid}')

    cpu = option['cpu']
    if cpu:
        cg = cgroup.CGroup('hogehoge')
        cg.set_cpu_limit(cpu)
        cg.add(pid)

    linux.sethostname('container-process')

    container = option['container']
    os.chroot(container.root_dir)
    os.chdir('/')

    command = option['commands']
    os.execvp(command[0], command)


def exec_run(image_name, cpu: float, commands: List[str]):
    registry, image, tag = fmt.parse_image_opt(image_name)
    image = next((v for v in local.find_images() if v.name == f'{registry}/{image}' and v.version == tag), None)
    print(f'running {image}')

    container = data.Container.init_from_image(image)

    linux.mount(
        'overlay',
        container.root_dir,
        'overlay',
        linux.MS_NODEV,
        f"lowerdir={image.content_dir},upperdir={container.rw_dir},workdir={container.work_dir}"
    )

    flags = linux.CLONE_NEWUTS
    option = {'cpu': cpu, 'commands': commands, 'container': container}
    pid = linux.clone(child_proc_callback, flags, (option,))

    os.waitpid(pid, 0)
