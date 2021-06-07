import os
from runpy import run_path

from setuptools import find_packages, setup


# read the program version from version.py (without loading the module)
__version__ = run_path('src/aws_client/version.py')['__version__']


def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="aws_client",
    version=__version__,
    author="David Kuda",
    author_email="david.kuda.ch@gmail.com",
    description="ETL from AWS S3 to AWS Redshift",
    license="",
    url="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={'azure_python_client': ['res/*']},
    long_description=read('README.md'),
    install_requires=[],
    tests_require=[],
    cmdclass={},
    platforms='any',
    python_requires='>=3.8',
)