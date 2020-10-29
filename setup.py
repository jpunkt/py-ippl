import re
import ast

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('pyippl/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

    setup(
        name='py_ippl',
        version=version,
        description='Python Image Processing Pipeline',
        url='https://github.com/jpunkt/pyippl.git',
        license='',
        author='Johannes Payr',
        author_email='johannes.payr@mci.edu',
        platforms='any',

        packages=[
            'pyippl'
        ],

        install_requires=[

        ],
    )
