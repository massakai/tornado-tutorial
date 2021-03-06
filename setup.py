from setuptools import setup, find_packages

from tutorial.__version__ import __version__

setup(
    name="tornado-tutorial",
    version=__version__,
    author="Sakai, Masashi",
    author_email="masashi.sakai1986@gmail.com",
    url="https://github.com/massakai/tornado-tutorial",
    packages=find_packages(),
    install_requires=[
        "oneagent-sdk==1.4.0.20210127.165413",
        "prometheus_client==0.8.0",
        "tornado==6.1",
    ],
    entry_points={
        'console_scripts': [
            'tutorial_server = tutorial.server:main',
        ],
    },
)
