from setuptools import setup


setup(
    name="ddate",
    version="0.0.3",
    author="Adam Talsma",
    author_email="adam@talsma.ca",
    packages=["ddate"],
    scripts=["bin/ddate"],
    url="https://github.com/a-tal/ddate",
    description="Discordian date",
    long_description=(
        "Converts and prints time using the Discordian calendar"
    ),
    download_url="https://github.com/a-tal/ddate",
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
