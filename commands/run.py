import linux
import os
from typing import List
import commands.cgroup as cgroup
import commands.data as data
import commands.format as fmt
import commands.local as local

def child_proc_callback(option: dict):
    pid = os.getpid()
    print(f"container pid: {pid}")
    
    linux.sethostname("container")
    
    cpu = option['cpu']
    if cpu:
    	cg = cgroup.CGroup('container')
    	cg.set_cpu_limit(cpu)
    	cg.add(pid)
    	
    container = option['container']
    image = option['image']
    linux.mount(
    	'overlay',
    	container.root_dir,
    	'overlay',
    	linux.MS_NODEV,
    	f"lowerdir={image.content_dir},upperdir={container.rw_dir},workdir={container.work_dir}"
    )
    
    os.chroot(container.root_dir)
    os.chdir('/')

    command = option['command']
    os.execvp(command[0], command)


def exec_run(image_name: str, cpu: float, command: List[str]):
    registry, image, tag = fmt.parse_image_opt(image_name)
    image = next((v for v in local.find_images() if v.name == f'{registry}/{image}' and v.version == tag), None)
    print(f'running {image}')
    
    container = data.Container.init_from_image(image)
    
    flags = (linux.CLONE_NEWUTS | # UTS名前空間
    	linux.CLONE_NEWPID# PID名前空間
    )
    
    option = {'cpu': cpu, 'command': command, 'container': container, 'image': image}
    
    child_pid = linux.clone(
        child_proc_callback,
        flags,
        (option, )
    )

    os.waitpid(child_pid, 0)

