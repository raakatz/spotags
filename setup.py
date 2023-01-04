from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="spotags",
    version="1.0.0",
    python_requires=">=3.10",
    install_requires=requirements,
    author="Raanan Katz",
    author_email="raakatz97@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/raakatz/spotags/",
    license="GPL-3.0",
    description="Manage Spotify album tags",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "spotags=spotags.main:spotags",
        ],
    },
)

