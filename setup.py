import os
import pathlib

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
        print(f"Successfully generated token {response}")
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


def _is_versions_equals(version_a, version_b):
    return version_a.compare(version_b) == 0


def _define_version(
    test_pypi_version: VersionInfo, pypi_version: VersionInfo
) -> VersionInfo:
    env: str = os.getenv("ENV")
    test_pypi_version_without_prerelease = VersionInfo(
        major=test_pypi_version.major,
        minor=test_pypi_version.minor,
        patch=test_pypi_version.patch,
    )

    if not test_pypi_version and not pypi_version:
        return VersionInfo.parse("1.0.0-rc.1")

    if _is_dev_env(env):
        if not pypi_version or not _is_versions_equals(
            test_pypi_version_without_prerelease, pypi_version
        ):
            return test_pypi_version.next_version(part="prerelease")
        else:
            return test_pypi_version.bump_minor().bump_prerelease()
    if _is_main_env(env):
        return test_pypi_version.finalize_version()


def _get_version() -> str:
    version: VersionInfo
    test_pypi_version: VersionInfo = TEST_PYPI_ADAPTER.get_version()
    pypi_version: VersionInfo = PYPI_ADAPTER.get_version()

    return str(_define_version(test_pypi_version, pypi_version))


# Package version
# VERSION = _get_version()
VERSION = "1.0.0-rc.1"

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
