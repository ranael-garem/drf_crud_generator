import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf_crud_generator',
    version='0.1',
    packages=find_packages(exclude=['main', 'generator']),
    include_package_data=True,
    install_requires=[
          'djangorestframework',
    ],
    license='BSD License',  # example license
    description='Genrate Model, View and Serializer with one command for Django rest framework',
    long_description=README,
    url='https://github.com/ranael-garem/drf_crud_generator',
    author='Your Name',
    author_email='ranasalehelgarem@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11.2',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
