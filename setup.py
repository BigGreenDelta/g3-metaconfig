import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="g3-config",
    version="0.0.8",
    author="Kirill Potapenko",
    author_email="ajiadb9@bgd.team",
    description="Simple metaclass to simplify work with argparse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://bgd.team",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=[
        "setuptools~=59.5.0",
        "ConfigArgParse~=1.5.3",
        "pydantic~=1.8.2",
        "wheel~=0.37.0",
    ],
    packages=["g3_config"],
    python_requires=">=3.8",
)
