import setuptools
from collections import OrderedDict

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="spotlight",
    version="1.0.0",
    author="Michiel Doesburg",
    author_email="michiel@moddix.com",
    description="Laravel style data validation for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mdoesburg/spotlight",
    project_urls=OrderedDict(
        (
            ("Documentation", "https://github.com/mdoesburg/spotlight"),
            ("Code", "https://github.com/mdoesburg/spotlight"),
        )
    ),
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[],
)
