from distutils.core import setup, Extension
setup(name='stdvec',
        version='1.0',
        ext_modules=[Extension('stdvec', ['lib.cpp'], language="c++")]
)

