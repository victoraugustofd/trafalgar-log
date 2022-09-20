import os
import pathlib

import pip

pip.main(["install", "semver", "uplink"])

from semver import VersionInfo
from setuptools import setup, find_packages
from uplink import Consumer, get, response_handler

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
TEST_PYPI_URL = "https://test.pypi.org"
PYPI_URL = "https://pypi.org"
PACKAGE_ENDPOINT = "/pypi/trafalgar-log/json"


def raise_for_status(response) -> VersionInfo:
    status_code: int = response.status_code

    if _is_success(status_code):
        Logger.info("Setup", "Successfully generated token.", response)
        return VersionInfo.parse(response.json().get("info").get("version"))


def _is_success(status_code: int):
    return 200 <= status_code < 300


class PyPIClient(Consumer):
    @response_handler(raise_for_status)
    @get(PACKAGE_ENDPOINT)
    def get_version(
        self,
    ) -> VersionInfo:
        """Generate new token."""


TEST_PYPI_ADAPTER = PyPIClient(base_url=TEST_PYPI_URL)
PYPI_ADAPTER = PyPIClient(base_url=PYPI_URL)


def _is_dev_env(env: str) -> bool:
    return env.lower() == "dev"


def _is_main_env(env: str) -> bool:
    return env.lower() == "main"


def _get_version() -> str:
    version: VersionInfo = VersionInfo.parse("1.0.0-rc1")
    test_pypi_version: VersionInfo = TEST_PYPI_ADAPTER.get_version()
    pypi_version: VersionInfo = PYPI_ADAPTER.get_version()
    env: str = os.getenv("ENV")

    if test_pypi_version or pypi_version:
        if test_pypi_version.compare(pypi_version) == -1:
            pass

        if _is_dev_env(env):
            version = pypi_version.next_version(part="prerelease")
        if _is_main_env(env):
            version = pypi_version.next_version(part="minor")

    return str(version)


# Package version
# VERSION = _get_version()
VERSION = "1.0.0-rc1"

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
    packages=find_packages(exclude="tests"),
    python_requires=">=3.7, <4",
    install_requires=["semver", "uplink", "dynaconf", "python-json-logger"],
    license="MIT",
)
