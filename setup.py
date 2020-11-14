from setuptools import setup, find_packages

import yaml


def get_version():
    with open("./openapi.yaml") as f:
        return yaml.load(f)["info"]["version"]


setup(
    name="tornado-tutorial",
    version=get_version(),
    author="Sakai, Masashi",
    author_email="masashi.sakai1986@gmail.com",
    url="https://github.com/massakai/tornado-tutorial",
    packages=find_packages(),
    install_requires=[
        "tornado==6.1",
    ]
)
