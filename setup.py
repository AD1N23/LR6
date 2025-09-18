# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize



ext = Extension(
    "fermat_cython",
    sources=["fermat_cython.pyx"],
)

setup(
    ext_modules=cythonize([ext])
)