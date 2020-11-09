import setuptools

with open("README.md") as fh:
    long_description = fh.read()

with open("VERSION") as fh:
    version = fh.read()

with open("DEPS.txt") as fh:
    dependencies = list(filter(None, fh.read().splitlines()))

setuptools.setup(
    name='hspylib',
    version=version,
    description='HomeSetup python3 library',
    author='Hugo Saporetti Junior',
    author_email='yorevs@hotmail.com',
    url="https://github.com/yorevs/hspylib",
    long_description=long_description,
    packages=setuptools.find_packages(
        exclude=[
            'resources',
            'test'
        ]
    ),
    package_data={
        'hspylib.core.crud.db.sql': ['sql_stubs.sql']
    },
    include_package_data=True,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=dependencies,
)
