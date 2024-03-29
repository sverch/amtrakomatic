"""
setup.py file

NOTE: This setup.py was lifted from https://github.com/kennethreitz/setup.py/blob/master/setup.py
and https://github.com/requests/requests/blob/master/setup.py.  So see there for more details.
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Used for looking up "<NAME>/__version__.py
NAME = 'amtrakomatic'

# What packages are required for this module to be executed?
REQUIRED = [
        'selenium',
        'ipython',
        'click',
        'fuzzywuzzy',
        'python-levenshtein',
        'pytest',
        'pylint',
        'bs4',
        'tox',
]

# What packages are required for this module to be tested?
TESTS_REQUIRED = []

# What packages are optional?
EXTRAS = {
    "testing": TESTS_REQUIRED
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for
# that!

here = os.path.abspath(os.path.dirname(__file__)) # pylint: disable=invalid-name

# Load the package's __version__.py module as a dictionary.
about = {} # pylint: disable=invalid-name
print(os.listdir(here))
print(os.listdir(os.path.join(here, NAME)))
with open(os.path.join(here, NAME, '__version__.py')) as f:
    # pylint: disable=exec-used
    exec(f.read(), about)

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        LONG_DESCRIPTION = '\n' + f.read()
        print(LONG_DESCRIPTION)
except FileNotFoundError:
    LONG_DESCRIPTION = about["__description__"]


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []
    user_options = [
        # The format is (long option, short option, description).
        ('use-test-index=', None,
         'Whether to use the test index.  Default is true, set to false to upload to real index.'),
    ]

    @staticmethod
    def status(message):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(message))

    def initialize_options(self):
        """
        Unused/noop
        """
        # pylint:disable=attribute-defined-outside-init
        self.use_test_index = "true"

    def finalize_options(self):
        """
        Unused/noop
        """

    def run(self):
        """
        Runs package upload
        """
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(
            sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        if self.use_test_index == "false":
            os.system('twine upload dist/*')

            # Only push git tags when uploading to real pypi
            self.status('Pushing git tags…')
            os.system('git tag v{0}'.format(about['__version__']))
            os.system('git push --tags')
        else:
            self.status('Using test index.  Run with "--use-test-index false" to use real pypi.')
            os.system('twine upload --repository-url https://test.pypi.org/legacy/ dist/*')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=about["__description__"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=about["__author__"],
    author_email=about["__author_email__"],
    python_requires=about["__requires_python__"],
    url=about["__url__"],
    packages=find_packages(exclude=('tests',)),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    scripts=['bin/amtrakomatic'],
    install_requires=REQUIRED,
    tests_require=TESTS_REQUIRED,
    extras_require=EXTRAS,
    package_data={'': ['amtrakomatic']},
    include_package_data=True,
    license=about["__license__"],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
