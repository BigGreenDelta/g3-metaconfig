import setuptools

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

with open("requirements.txt", "r", encoding="utf-8") as reqs_file:
    install_reqs = reqs_file.read().splitlines()

setuptools.setup(
    name="g3-metaconfig",
    version="1.1.1",
    author="Kirill Potapenko",
    author_email="ajiadb9@bgd.team",
    description="Simple metaclass to simplify work with argparse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BigGreenDelta/g3-metaconfig",
    project_urls={
        "Site": "http://bgd.team",
        "Bug Tracker": "https://github.com/BigGreenDelta/g3-metaconfig/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    install_requires=install_reqs,
    packages=["g3_metaconfig", "g3_metaconfig.tests"],
    python_requires=">=3.8",
)
