import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Package version
VERSION = "1.0.0-rc3"

setup(
    name="trafalgar-log",
    version=VERSION,
    description="A log framework that prints logs as JSON.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/victoraugustofd/trafalgar-log",
    author="victoraugustofd",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Topic :: System :: Logging",
    ],
    keywords="logs",
    package_dir={"": "trafalgar_log"},
    packages=find_packages(where="trafalgar_log", exclude="tests"),
    python_requires=">=3.7, <4",
    install_requires=["dynaconf", "python-json-logger"],
    license="MIT",
)
