from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys

# Custom install command to handle post-installation tasks
class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        install.run(self)
        print("Thank you for installing Quantum Ledger Core!")
        print("Please refer to the documentation for setup instructions.")

# Read the long description from the README file
def read_long_description():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Define package metadata
setup(
    name="quantum-ledger-core",
    version="0.1.0",
    author="KOSASIH",
    author_email="kosasihg88@gmail.com",
    description="A cutting-edge blockchain framework leveraging quantum computing principles.",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/KOSASIH/quantum-ledger-core",
    packages=find_packages(exclude=["tests*", "docs"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "web3>=5.0.0",
        "cryptography>=3.0.0",
        "requests>=2.25.0",
        "flask>=2.0.0",  # Example of a web framework dependency
        "sqlalchemy>=1.4.0",  # Example of a database ORM dependency
    ],
    entry_points={
        'console_scripts': [
            'quantum-ledger=quantum_ledger_core.cli:main',  # Command-line interface entry point
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
    include_package_data=True,
    zip_safe=False,
)
