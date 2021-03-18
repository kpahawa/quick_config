import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quick_config",
    version="0.2.0",
    author="Karan Pahawa",
    author_email="kpahawa@gmail.com",
    description="A thin and smart config provider for python apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kpahawa/quick_config",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
