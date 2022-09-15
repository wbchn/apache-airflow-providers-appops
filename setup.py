
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

"""Perform the package airflow-provider-appops setup."""
setup(
    name='airflow-provider-appops',
    version="0.0.4",
    description='App ops provider package built by papaya.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="wb",
    author_email="wbin.chn@gmail.com",
    maintainer="wbchn",
    maintainer_email="wbin.chn@gmail.com",
    entry_points={
        "apache_airflow_provider": [
            "provider_info=appops.__init__:get_provider_info"
        ]
    },
    license='Apache License 2.0',
    packages=['appops', 'appops.hooks',
              'appops.operators'],
    install_requires=['apache-airflow>=2.1,<2.3', 'apache-airflow-providers-google>=5.0.0,<7.0.0', 'protobuf<=3.20.2'],
    setup_requires=['setuptools', 'wheel'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
    ],
    url='https://github.com/wbchn/apache-airflow-providers-appops',
    python_requires='~=3.7',
)
