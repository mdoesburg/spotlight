import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='spotlight',
    version='0.1.2',
    author='Michiel Doesburg',
    author_email='michiel@moddix.com',
    description='Laravel style input validation for Python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mdoesburg/spotlight',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[]
)
