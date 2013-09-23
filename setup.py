# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-tests-assistant',
    version='0.3.0',
    description= 'A tool to help keep track of tests, specially for you - developer.',
    license='(AGPL v3+) GNU AFFERO GENERAL PUBLIC LICENSE Version 3 or later',
    url='https://github.com/tests-assistant/tests-assistant/',
    author=u'Amirouche Boubekki',
    author_email='amirouche.boubekki@gmail.com',
    maintainer=u'Arun Karunagath',
    maintainer_email='the1.arun@gmail.com',
    packages=find_packages(),
    long_description=open('README.rst').read(),
    install_requires=open('requirements.txt').readlines(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False,
)

