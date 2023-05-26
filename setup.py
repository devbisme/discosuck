#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "requests",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Dave Vandenbout",
    author_email="devb@xess.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Suck posts from a Discourse forum.",
    entry_points={
        "console_scripts": [
            "discosuck=discosuck.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="discosuck",
    name="discosuck",
    packages=find_packages(include=["discosuck", "discosuck.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/devbisme/discosuck",
    project_urls={
        # "Documentation": "https://devbisme.github.io/discosuck",
        "Documentation": "https://github.com/devbisme/discosuck",
        "Source": "https://github.com/devbisme/discosuck",
        "Changelog": "https://github.com/devbisme/discosuck/blob/master/HISTORY.rst",
        "Tracker": "https://github.com/devbisme/discosuck/issues",
    },
    version="0.1.0",
    zip_safe=False,
)
