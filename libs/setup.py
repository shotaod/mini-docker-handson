from setuptools import setup, Extension

linux_module = Extension('linux', sources=['linux.c'])
setup(name='linux', nversion='1.0', description='linux syscall wrapper', ext_modules=[linux_module])