from distutils.core import setup

import setuptools

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="kloppy-spark",
    version="0.0.2",
    author="Felix Schmdit",
    author_email="info@deepsports.io",
    url="https://deepsports.io",
    packages=setuptools.find_packages(exclude=["tests"]),
    license="BSD",
    description="Spark Tools to work with Kloppy",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=[
        "kloppy>=1.4.4",
        "pyspark>=3.0.1",
    ],
    extras_require={
        "test": ["pytest", "pandas>=1.0.0"],
        "development": ["pre-commit"],
    },
)
