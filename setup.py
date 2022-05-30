import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="relsad",
    version="0.0.1",
    author="Stine Fleischer Myhre",
    author_email="stine.f.myhre@ntnu.no",
    description="A Python package for reliability assessment of modern distribution systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stinefm/STNetwork",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
