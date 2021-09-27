from __future__ import division, print_function, absolute_import
import io
import re
import setuptools


with io.open('backend/__init__.py', 'rt', encoding='utf8') as file:
    VERSION = re.search(r'__version__ = \'(.*?)\'', file.read()).group(1)


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()


CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.7
Topic :: Software Development
Operating System :: POSIX
Operating System :: Unix
"""


def setup_package():
    from setuptools import setup
    metadata = dict(
        name='postgis-crud-rest',
        version=VERSION,
        maintainer="dmitrii-zagornyi",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/dmitrii-zagornyi/postgis-crud-rest",
        author="dmitrii-zagornyi",
        license='GNU General Public License v3.0',
        classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
        platforms=["Linux"],
        test_suite='nose.collector',
        python_requires='>=3.7',
        setup_requires=['setuptools'],
        install_requires=[],
        packages=['backend'],
        ext_modules=None
    )
    setup(**metadata)

    return None


if __name__ == '__main__':
    setup_package()
