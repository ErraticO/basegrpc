from setuptools import setup
from pathlib import Path

NAME = 'basegrpc'
VERSION = '0.0.1'

# define the extension packages to include
# ----------------------------------------

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# define the main package setup function
# --------------------------------------

setup(
    name=NAME,
    version=VERSION,
    description='A General Service Framework for gRPC',
    author='ErraticO',
    author_email='wyh123132@163.com',
    url='https://github.com/ErraticO/basegrpc',
    keywords=['machine', 'learning', 'recommendation', 'service', 'grpc'],
    license='GNU General Public License v3.0',
    packages=['basegrpc'],
    zip_safe=False,
    python_requires='>=3.7',
    long_description=long_description,
    long_description_content_type="text/markdown",
)

