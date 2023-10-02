from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="romanization",
    version="1.0.0",
    author="Joumaico Maulas",
    description="Revised Romanization of Korean",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/joumaico/romanization",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=[
        "romanization",
    ],
    package_dir={
        "romanization": "src/romanization",
    },
    package_data={
        "romanization": [
            "convert/data/latin/*",
            "convert/data/raw/*",
            "convert/data/provisions",
            "convert/output/latin/*",
            "convert/output/raw/*",
        ]
    },
    python_requires=">=3.7",
    install_requires=[
        "numpy",
    ],
)
