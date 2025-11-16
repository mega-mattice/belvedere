from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="belvedere",
    version="0.6.0",
    author="Adam Pash",
    author_email="adam.pash@gmail.com",
    description="Automated file management application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mega-mattice/belvedere",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PySide6>=6.6.0",
        "watchdog>=3.0.0",
        "send2trash>=1.8.2",
    ],
    entry_points={
        "console_scripts": [
            "belvedere=belvedere.main:main",
        ],
    },
    package_data={
        "belvedere": ["resources/*"],
    },
)
