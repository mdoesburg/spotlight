import re

from setuptools import setup, find_packages
from collections import OrderedDict

with open("README.md", "r") as f:
    long_description = f.read()

with open("src/spotlight/__init__.py", encoding="utf8") as f:
    description = f.readline().strip('"\n')
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="spotlight",
    version=version,
    author="Michiel Doesburg",
    author_email="michiel@moddix.com",
    description=description,
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
    python_requires=">=3.6",
)
