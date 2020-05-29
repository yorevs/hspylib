import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='hhs-pylib',
    version='0.9.0',
    description='HomeSetup python3 library',
    author='Hugo Saporetti Junior',
    author_email='yorevs@hotmail.com',
    packages = setuptools.find_packages(),
    url='https://github.com/yorevs/hhs-pylib'
)
