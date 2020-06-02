import setuptools

with open("README.md") as fh:
    long_description = fh.read()

with open("VERSION") as fh:
    version = fh.read()

setuptools.setup(
    version=version,
    description='HomeSetup python3 library',
    author='Hugo Saporetti Junior',
    author_email='yorevs@hotmail.com',
    url='https://github.com/yorevs/hhs-pylib',
    name='hspylib',
    long_description=long_description,
    packages=['hspylib'],
    license='MIT',
    install_requires=[
        'PyQt5',
        'cryptography',
        'pycodestyle',
        'pymysql',
        'requests'
    ],
)
