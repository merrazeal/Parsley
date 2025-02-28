from os.path import dirname, join

from setuptools import find_packages, setup

setup(
    name="parsley",
    version="0.3.2",
    packages=find_packages(),
    long_description=open(join(dirname(__file__), "README.md")).read(),
    install_requires=[
        "asyncio==3.4.3",
        "async-timeout==5.0.1",
        "pydantic==2.10.1",
        "pydantic-settings==2.6.1",
        "backoff==2.2.1",
    ],
    extras_require={
        "redis": ["redis==5.2.0"],
        "rabbitmq": ["aio-pika==9.5.3"],
    },
)
