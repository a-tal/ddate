from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """Shim in pytest to be able to use it with setup.py test."""

    def finalize_options(self):
        """Stolen from http://pytest.org/latest/goodpractises.html."""

        TestCommand.finalize_options(self)
        self.test_args = ["-v", "-rf", "--cov", "ddate"]
        self.test_suite = True

    def run_tests(self):
        """Also shamelessly stolen."""

        # have to import here, outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


setup(
    name="ddate",
    version="0.0.7",
    author="Adam Talsma",
    author_email="adam@talsma.ca",
    packages=["ddate"],
    install_requires=["dateandtime"],
    entry_points={"console_scripts": [
        "ddate = ddate.base:main",
        "dcal = ddate.dcal:main",
    ]},
    url="https://github.com/a-tal/ddate",
    description="Discordian date",
    long_description=(
        "Converts and prints time using the Discordian calendar"
    ),
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
