from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pymixology",
    version="0.1.0",
    author="Data 533 Group 6",
    author_email="example@example.com",
    description="A cocktail inventory and recommendation package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/data533_group6_step3",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        "pymixology": ["data/*.json"],
    },
    install_requires=[
    ],
)

