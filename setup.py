from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bingsearch",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
    ],
    author="tangkewang",
    author_email="3188422067@qq.com",
    description="Bing Search API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tangkewang/bingsearch",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
