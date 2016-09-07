from setuptools import setup

import os

# Put here required packages
packages = ['Django<=1.6', 'django-redis-cache', 'hiredis',]


setup(name='MojBlog',
      version='1.0',
      description='OpenShift App',
      author='Joanna',
      author_email='kotka5351@gmail.com',
      url='https://pypi.python.org/pypi',
      install_requires=packages,
)

