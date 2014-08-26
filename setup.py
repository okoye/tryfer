from setuptools import setup, find_packages

setup(
    name='pyzipkin',
    version='0.23',
    description='Zipkin Tracing Library',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
    maintainer='Chuka',
    maintainer_email='contact@chookah.org',
    license='APL2',
    url='https://github.com/okoye/pyzip',
    long_description=open('README.rst').read(),
    packages=find_packages('.'),
    install_requires=[
        'thrift == 0.8.0',
    ],
)
