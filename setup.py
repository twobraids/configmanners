
# Can't import unicode_literals in setup.py currently
# http://stackoverflow.com/a/23175131
import codecs
import os
from setuptools import setup
import sys


# Prevent spurious errors during `python setup.py test`, a la
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html:
try:
    import multiprocessing
except ImportError:
    pass

if sys.version_info[0] == 3 and sys.version_info[1] < 8:
    print("Please upgrade to a python >= 3.8!", file=sys.stderr)
    sys.exit(1)


def read(fname):
    fpath = os.path.join(os.path.dirname(__file__), fname)
    with codecs.open(fpath, 'r', 'utf8') as f:
        return f.read().strip()


setup(
    name='configmanners',
    version="3.0",
    description=(
        'Flexible reading and writing of namespaced configuration options'
    ),
    long_description=read('README.md'),
    author='K Lars Lohn',
    author_email='twobraids@gmail.com',
    url='https://github.com/twobraids/configmanners',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Developers',
        'Environment :: Console',
    ],
    packages=['configmanners'],
    package_data={'configmanners': ['*/*', 'version.txt']},
    install_requires=[
        'configobj',
    ],
    tests_require=[
        'mock'
    ],
    test_suite='',
    zip_safe=False,
),
