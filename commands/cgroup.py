from cgroups import cgroup


class CGroup:
    name: str
    cg: cgroup.Cgroup

    def __init__(self, name: str):
        self.name = name
        self.cg = cgroup.Cgroup(name)

    def add(self, pid: int):
        self.cg.add(pid)

    def set_cpu_limit(self, limit: float):
        if 'cpu' in self.cg.cgroups:
            cpu_period_file = self.cg._get_cgroup_file('cpu', 'cpu.cfs_period_us')
            cpu_quota = self.cg._get_cgroup_file('cpu', 'cpu.cfs_quota_us')

            with open(cpu_period_file) as period_f, open(cpu_quota, 'w') as quota_f:
                period = int(period_f.read())
                quota = int(period * limit)
                quota_f.write(f'{quota}')
        else:
            raise cgroup.CgroupsException('CPU hierarchy not available in this cgroup')
