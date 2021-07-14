import linux


def child_proc_callback():
    print('hello world')


def exec_run():
    # lesson 1.
    flags = 0
    linux.clone(child_proc_callback, flags, ())
