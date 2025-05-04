from setuptools import setup, find_packages

setup(
    name="fashion-mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mcp[cli]>=1.7.1",
        "python-dotenv"
    ]
)