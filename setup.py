#!/usr/bin/env python3

import os
import re

from setuptools import find_packages, setup

NAME = "gimeltra"


def get_absolute_path(*args):
    """Transform relative pathnames into absolute pathnames."""
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, *args)


with open(get_absolute_path("README.md"), encoding='utf-8') as f:
    long_description = f.read()


def get_version(*args):
    verstrline = open(get_absolute_path(NAME, "__init__.py"), "rt", encoding='utf-8').read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        return mo.group(1)
    return "undefined"


def get_requirements(*args):
    """Get requirements from pip requirement files."""
    requirements = set()
    with open(get_absolute_path(*args), encoding='utf-8') as handle:
        for line in handle:
            # Strip comments.
            line = re.sub(r"^#.*|\s#.*", "", line)
            # Ignore empty lines
            if line and not line.isspace():
                requirements.add(re.sub(r"\s+", "", line))
    return sorted(requirements)


setup(
    name=f"{NAME}",
    version=get_version(),
    description="Simple transliteration tool for mostly Semitic languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Adam Twardoch",
    author_email="adam+github@twardoch.com",
    url=f"https://github.com/twardoch/{NAME}/",
    project_urls={"Source": f"https://github.com/twardoch/{NAME}/"},
    license="GPLv2",
    download_url=f"https://github.com/twardoch/{NAME}/",
    python_requires=">=3.9",
    install_requires=get_requirements("requirements.txt"),
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    keywords=[
        "dictionary",
        "wiktionary",
        "transliteration",
        "transliterate",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
    ],
    entry_points=f"""
        [console_scripts]
        {NAME}py={NAME}.__main__:main
        """,
)
