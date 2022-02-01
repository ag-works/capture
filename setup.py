from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Python package that captures exceptions and notify them'
LONG_DESCRIPTION = 'Python package that captures exceptions and notify them'

setup(
    name="capture-errors", 
    version=VERSION,
    author="Ashish Garg",
    author_email="ashish.garg@linux.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    include_package_data=True,
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "jinja2": [],
        "requests": [],
    },
    keywords=['python', 'exceptions', 'errors'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
    ]
)
