import codecs
import os
import re
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*folders):
    with codecs.open(os.path.join(here, *folders), encoding='utf-8') as fd:
        return fd.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file,
                              re.M)
    if version_match:
        return version_match.group(1)

    raise RuntimeError("ERROR: version not found")


def get_requirements(file_name):
    requires_file = read('requirements', file_name)
    return requires_file.splitlines()


setup(
    name='ggit',

    version=find_version('ggit', '__init__.py'),

    description='GPG git tool',
    long_description=read('README.md'),

    url='https://github.com/pahumadad/ggit',

    license='',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: System',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='git gpg',
    install_requires=get_requirements('default.txt'),
    setup_requires=get_requirements('test.txt'),
    test_suite='test',
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={'console_scripts': ['ggit = ggit.__main__:main']}
)
