import io
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """Shim in pytest to be able to use it with setup.py test."""

    def finalize_options(self):
        """Stolen from http://pytest.org/latest/goodpractises.html."""

        TestCommand.finalize_options(self)
        self.test_args = ["-v", "-rf", "--cov", "ddate", "--cov-report",
                          "term-missing", "tests"]
        self.test_suite = True

    def run_tests(self):
        """Also shamelessly stolen."""

        # have to import here, outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


with io.open("README.rst", encoding="utf-8") as openreadme:
    long_description = openreadme.read()


setup(
    name="ddate",
    version="0.1.2",
    author="Adam Talsma",
    author_email="adam@talsma.ca",
    packages=["ddate"],
    install_requires=["dateandtime"],
    entry_points={"console_scripts": [
        "ddate = ddate.base:main",
        "dcal = ddate.dcal:main",
    ]},
    url="http://a-tal.github.io/ddate",
    description="Discordian date and calendar",
    long_description=long_description,
    download_url="https://github.com/a-tal/ddate",
    cmdclass={"test": PyTest},
    tests_require=["pytest", "pytest-cov"],
    license="BSD",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
)
