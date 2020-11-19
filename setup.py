from setuptools import setup

setup(
    name="webstories",
    version="0.0.1",
    packages=["webstories"],
    test_suite="tests",
    url='https://github.com/torchbox/webstories/',
    author="Matt Westcott",
    author_email="matthew@torchbox.com",
    description="Parser for AMP web stories",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "beautifulsoup4>=4.6,<5",
        "bleach>=3.2,<4",
    ],
    license="BSD",
)
