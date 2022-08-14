from setuptools import setup, find_packages

setup(
    name="PTP",
    version="1.0.1",
    description="pygame to pillow",
    author="andrew",
    project_urls={
        "Repository": "https://github.com/andrewthederp/PTP",
        "Issue tracker": "https://github.com/andrewthederp/PTP/issues",
    },
    maintainer="Marcus",
    url="https://github.com/andrewthederp/PTP",
    license="Apache",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=["pillow"],
    python_requires=">=3.6",
    packages=find_packages(include=["ptp", "ptp.*"]),
)
