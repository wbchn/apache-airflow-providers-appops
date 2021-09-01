
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

"""Perform the package airflow-provider-appops setup."""
setup(
    name='airflow-provider-appops',
    version="0.0.2",
    description='App ops provider package built by papaya.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        "apache_airflow_provider": [
            "provider_info=appops.__init__:get_provider_info"
        ]
    },
    license='Apache License 2.0',
    packages=['appops', 'appops.hooks',
              'appops.operators'],
    install_requires=['apache-airflow>=2.1', 'apache-airflow-providers-google>=5.0.0'],
    setup_requires=['setuptools', 'wheel'],
    author='wb',
    author_email='wb@papaya*mobile.com',
    url='http://papaya.io/',
    python_requires='~=3.7',
)