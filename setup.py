# coding:utf-8

import sys
from setuptools import setup, find_packages

if sys.version_info <= (2, 6):
    error = 'ERROR: qingcloud-sdk requires Python Version 2.6 or above.'
    print >> sys.stderr, error
    sys.exit(1)

DEBUG = True

if DEBUG:
    pkg = {
        'name': 'simon-test-sdk',
        'version': '0.1.3',
        'description': 'Software Development Kit.',
        'long_description': '',
        'keywords': 'iaas sdk',
        'url': '',
    }
else:
    pkg = {
        'name': 'qingcloud-sdk',
        'version': '0.1',
        'description': 'Software Development Kit for QingCloud.',
        'long_description': open('README.rst', 'rb').read().decode('utf-8'),
        'keywords': 'qingcloud iaas sdk',
        'url': 'https://docs.qingcloud.com/sdk/',
        }

setup(
    name = pkg['name'],
    version = pkg['version'],
    description = pkg['description'],
    long_description = pkg['long_description'],
    keywords = pkg['keywords'],
    author = 'Yunify Team',
    author_email = 'simon@yunify.com',
    url = pkg['url'],
    packages = find_packages('.'),
    package_dir = {pkg['name']: 'qingcloud'},
    include_package_data = True,
    install_requires = [
        'PyYAML>=3.1',
    ]
)
