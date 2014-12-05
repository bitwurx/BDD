from setuptools import setup

setup(
    version="0.1",
    name="BDD",
    description="Behavior Driven Developmet Testing",
    url="https://github.com/bitwurx/BDD",
    author="Jared Patrick",
    author_email="jared.patrick@gmail.com",
    license="MIT",
    packages=['bdd'],
    install_requires=['termcolor'],
    scripts=['scripts/bdd']
)
