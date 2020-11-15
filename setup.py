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
        "tornado==6.1",
    ],
    entry_points={
        'console_scripts': [
            'tutorial_server = tutorial.server:main',
        ],
    },
)
