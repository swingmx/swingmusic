"""
Minimal setup.py that forces setuptools to produce a platform-tagged wheel
when Nuitka-compiled .so/.pyd extension modules are present in the package.

Without this, setuptools sees only .py files (and package_data) and emits a
pure-Python `py3-none-any` wheel — which cibuildwheel rightfully rejects.
"""

from setuptools import setup
from setuptools.dist import Distribution


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


setup(distclass=BinaryDistribution)
