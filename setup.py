import setuptools
from collections import OrderedDict

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='spotlight',
    version='0.2.0',
    author='Michiel Doesburg',
    author_email='michiel@moddix.com',
    description='Laravel style input validation for Python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mdoesburg/spotlight',
    project_urls=OrderedDict((
        ('Documentation', 'https://github.com/mdoesburg/spotlight'),
        ('Code', 'https://github.com/mdoesburg/spotlight')
    )),
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[]
)
