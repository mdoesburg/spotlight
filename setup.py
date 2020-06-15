from setuptools import setup, find_packages
from collections import OrderedDict

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="spotlight",
    version="1.0.8",
    author="Michiel Doesburg",
    author_email="michiel@moddix.com",
    description="Laravel style data validation for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="spotlight validation validate",
    url="https://github.com/mdoesburg/spotlight",
    project_urls=OrderedDict(
        (
            ("Documentation", "https://github.com/mdoesburg/spotlight"),
            ("Code", "https://github.com/mdoesburg/spotlight"),
        )
    ),
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[],
)
