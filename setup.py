from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name="romanization",
    version="1.1.0",
    author="Joumaico Maulas",
    description="Revised Romanization of Korean",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/joumaico/romanization",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    packages=[
        "romanization",
    ],
    package_dir={
        "romanization": "src/romanization",
    },
    python_requires=">=3.8",
)
