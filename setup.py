from setuptools import setup, find_packages


version = '0.1'

with open("README.md", "rb") as f:
    long_description = f.read().decode("utf-8")

setup(
    name='report-creator',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['report_creator = rmct.rmct:main']
    },
    version=version,
    description='A CLI tool for managing RM dev environment.',
    long_description=long_description,
    author='Kirill',
    author_email="kirill.leskin@dxc.com",
    install_requires=[
        'conlo>=0.3',
        'colorama',
        'PyYAML',
    ]
)
