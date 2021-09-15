from distutils.core import setup
from Cython.Build import cythonize
import shutil

shutil.copy("sp.py", "sp.pyx")


setup(
     ext_modules=cythonize("sp.pyx"),
)
