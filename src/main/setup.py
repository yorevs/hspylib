import setuptools

with open("README.md") as fh:
    long_description = fh.read()

with open("VERSION") as fh:
    version = fh.read()

setuptools.setup(
    name='hhs-pylib',
    version=version,
    description='HomeSetup python3 library',
    long_description=long_description,
    author='Hugo Saporetti Junior',
    author_email='yorevs@hotmail.com',
    packages = setuptools.find_packages(),
    url='https://github.com/yorevs/hhs-pylib'
)
