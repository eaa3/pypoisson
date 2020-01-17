import os
from distutils.core import setup
from setuptools import dist
dist.Distribution().fetch_build_eggs(['Cython', 'numpy'])

from distutils.extension import Extension
from Cython.Distutils import build_ext


    
def set_builtin(name, value):
    if isinstance(__builtins__, dict):
        __builtins__[name] = value
    else:
        setattr(__builtins__, name, value)
    
class build_ext_pypoisson(build_ext):
    
    def finalize_options(self):
        build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        set_builtin('__NUMPY_SETUP__', False)
        import numpy

        self.include_dirs.append(numpy.get_include())
    
    def run(self):
    
        # Call original build_ext command
        build_ext.run(self)


sources = ["src/pypoisson.pyx"]
path = "src/PoissonRecon_v6_13/src/"
files = [os.path.join(path,x) for x in os.listdir(path) if x.endswith(".cpp")]
sources += files


exts = [Extension("pypoisson", sources,
        language="c++",
        extra_compile_args = ["-w","-fopenmp"],
        extra_link_args=["-fopenmp"]
        )]

setup(
    name='pypoisson',
    version='0.10',
    description='Poisson Surface Reconstruction Python Binding',
    author='Miguel Molero-Armenta',
    author_email='miguel.molero@gmail.com',
    url='https://github.com/mmolero/pypoisson',
    setup_requires=['numpy','cython'],
    install_requires=['numpy', 'cython'],
    cmdclass = {'build_ext': build_ext_pypoisson},
    ext_modules = exts
)
