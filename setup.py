# coding:utf-8

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (2, 6):
    error = 'ERROR: qingcloud-sdk requires Python Version 2.6 or above.'
    print >> sys.stderr, error
    sys.exit(1)


setup(
    name='qingcloud-sdk',
    version='1.0.13',
    description='Software Development Kit for QingCloud.',
    long_description=open('README.rst', 'rb').read().decode('utf-8'),
    keywords='qingcloud iaas qingstor sdk',
    author='Yunify Team',
    author_email='simon@yunify.com',
    url='https://docs.qingcloud.com/sdk/',
    packages=['qingcloud', 'qingcloud.conn', 'qingcloud.iaas',
              'qingcloud.misc', 'qingcloud.qingstor'],
    package_dir={'qingcloud-sdk': 'qingcloud'},
    namespace_packages=['qingcloud'],
    include_package_data=True,
    install_requires=['future']
)
