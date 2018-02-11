#!/usr/bin/env python

from setuptools import setup

setup(name="buildok",
    packages=[
        "buildok",
        "buildok.readers",
        "buildok.statements",
        "buildok.util",
    ],
    entry_points = {
        "console_scripts": [
            "build = buildok.bootstrap:main"
        ]
    },
    version="0.1",
    description="A tool to automate build steps from README files.",
    author="Alexandru Catrina",
    author_email="alex@codeissues.net",
    license="MIT",
    url="https://github.com/lexndru/buildok",
    download_url="https://github.com/lexndru/buildok/archive/v0.1.tar.gz",
    keywords=[
        "build-tool",
        "build-automation",
        "readme",
        "buildok"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
    ],
)