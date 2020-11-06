import setuptools

with open("README.md") as fh:
    long_description = fh.read()

with open("VERSION") as fh:
    version = fh.read()

setuptools.setup(
    name='hspylib',
    version=version,
    description='HomeSetup python3 library',
    author='Hugo Saporetti Junior',
    author_email='yorevs@hotmail.com',
    url="https://github.com/yorevs/hspylib",
    long_description=long_description,
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'PyQt5',
        'PyQt5-stubs',
        'cryptography',
        'pycodestyle',
        'pymysql',
        'requests'
    ],
)
