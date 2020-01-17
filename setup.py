import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


class CustomBuildExtCommand(build_ext):
    """build_ext command for use when numpy headers are needed."""
    def run(self):

        # Import numpy here, only when headers are needed
        import numpy

        # Add numpy headers to include_dirs
        self.include_dirs.append(numpy.get_include())

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
    setup_requires=['numpy'],
    install_requires=['numpy'],
    cmdclass = {'build_ext': CustomBuildExtCommand},
    ext_modules = exts
)
