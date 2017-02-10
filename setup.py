import codecs
import os
import re
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

with open('cuttle/__init__.py', 'r') as f:
    for l in f:
        if 'version' in l:
            version = l.split("'")[1]
            break

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cuttle',
      # uses semantic versioning scheme
      version=version,
      description='A simple ORM',
      long_description=long_description,
      url='https://github.com/smitchell556/cuttle',
      author='Spencer Mitchell',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
      ],
      keywords='sql mysql orm',
      packages=['cuttle'],
      include_package_data=True,
      dependency_links=['https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-2.1.5.zip'],
      install_requires=['mysql-connector-python'],
      setup_requires=['pytest-runner'],
      tests_require=[
          'pytest',
          'pytest-cov'
      ]
)
