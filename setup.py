    
import os
import sys

this_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(this_dir, 'src'))

from sst import __version__


NAME = 'sst'
PACKAGES = ['sst',]
SCRIPTS = ['sst-run', 'sst-remote']
DESCRIPTION = 'SST Web Test Framework'
URL = 'http://testutils.org/sst'

readme = os.path.join(this_dir, 'README')
LONG_DESCRIPTION = open(readme).read()

requirements = os.path.join(this_dir, 'requirements.txt')
REQUIREMENTS = filter(None, open(requirements).read().splitlines())

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Testing',
    'Topic :: Internet :: WWW/HTTP :: Browsers',
]

AUTHOR = 'Canonical ISD Team'
AUTHOR_EMAIL = 'corey@goldb.org'
KEYWORDS = ('selenium webdriver test testing web automation').split(' ')

params = dict(
    name=NAME,
    version=__version__,
    packages=PACKAGES,
    scripts=SCRIPTS,
    package_dir={'': 'src'},
    install_requires = REQUIREMENTS,
    
    # metadata for upload to PyPI
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    keywords=KEYWORDS,
    url=URL,
    classifiers=CLASSIFIERS,
)

from setuptools import setup
setup(**params)
