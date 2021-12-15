import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_reqs = f.read().splitlines()

setuptools.setup(
    name="g3-config",
    version="0.1.0",
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
    install_requires=install_reqs,
    packages=["g3_config", "g3_config.tests"],
    python_requires=">=3.8",
)
