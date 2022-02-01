from setuptools import setup, find_packages
import io
import os

VERSION = "0.0.1"


def get_long_description():
    with io.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="ouseful-sqlite-search-utils",
    description="Custom Pyhton functions for extending sqlite3 search.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Tony Hirst",
    version=VERSION,
    license="MIT License",
    packages=find_packages(),
    install_requires=[
        "sqlite_utils",
        "regex",
        "fuzzysearch",
        "spacy",
        "spaczz",
        "language_tool_python"
    ],
    extras_require={
    },
    entry_points="""
    """,
    url="https://github.com/innovationOUtside/ouseful-sqlite-search-utils",
    project_urls={
        "Source code": "https://github.com/innovationOUtside/ouseful-sqlite-search-utils",
        "Issues": "https://github.com/innovationOUtside/ouseful-sqlite-search-utils/issues",
    },
    python_requires=">=3.6",
    classifiers=[
        "Topic :: Database",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=False,
)