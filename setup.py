#
# Panya Analytics
#

from setuptools import setup, find_packages


setup(
    name='panya-analytics',
    version='0.0.1',
    description='Panya app facilitating tracking of arbitrary simple metrics.',
    long_description=open('README.rst', 'rt').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='https://github.com/praekelt/panya-analytics',
    packages=find_packages(),
    install_requires=[
        'django_geckoboard>=1.1.0',
    ],
    include_package_data=True,
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False,
)

