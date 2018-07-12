#!/usr/bin/env python

from setuptools import setup


long_description = """
Hap! is an HTML parser and scraping tool written in Python.

The purpose of Hap! is to have a simple and fast way to retrieve certain data from the internet. It uses JSON formatted data as input and output. Input can be either from a local file or from stdin from another process. Output is either printed to stdout or saved to file. If input is provided by file, Hap! names it dataplan ("data planning") and the same file is used when the output is saved.
"""

setup(name="buildok",
    packages=[
        "buildok",
        "buildok.readers",
        "buildok.statements",
        "buildok.structures",
        "buildok.util",
        "buildok.converters",
    ],
    entry_points = {
        "console_scripts": [
            "build = buildok.bootstrap:main"
        ]
    },
    version="0.3.0",
    description="A tool to automate build steps from README files.",
    long_description=long_description,
    author="Alexandru Catrina",
    author_email="alex@codeissues.net",
    license="MIT",
    url="https://github.com/lexndru/buildok",
    download_url="https://github.com/lexndru/buildok/archive/v0.3.0.tar.gz",
    keywords=["build-tool", "build-automation", "readme", "buildok"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
    ],
)
