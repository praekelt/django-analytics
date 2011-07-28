from setuptools import setup, find_packages
from setuptools.command.test import test

class TestRunner(test):
    def run(self, *args, **kwargs):
        if self.distribution.install_requires:
            self.distribution.fetch_build_eggs(self.distribution.install_requires)
        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(self.distribution.tests_require)
        from runtests import runtests
        runtests()

setup(
    name='django-analytics',
    version='0.0.1',
    description='Django app facilitating tracking of arbitrary simple metrics.',
    long_description=open('README.rst', 'rt').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='https://github.com/praekelt/django-analytics',
    packages=find_packages(),
    install_requires=[
        'django_geckoboard>=1.1.0',
    ],
    tests_require=[
        'django',
    ],
    include_package_data=True,
    test_suite = "analytics.tests",
    cmdclass={"test": TestRunner},
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

