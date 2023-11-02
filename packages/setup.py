from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'YOUR PACKAGE DESCRIPTION'

with open("README.md", "r") as f:
    long_description = f.read()

# Setting up
setup(
    name="YOUR PACKAGE NAME HERE",
    version=VERSION,
    author="Phonki",
    author_email="<phonkibusiness@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["numpy"], # this is an example package
    keywords=['python', 'chess'], # these are examples of keywords that will help users find your package
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
    ]
)

"""
----- build commands -----

(delete all build files first)

python3 setup.py sdist bdist_wheel
twine upload dist/* --verbose
"""