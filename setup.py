from setuptools import setup, find_packages

setup(
    name="update_if_current",
    version="0.1.0",
    description="A description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/agumbe-ai/python-mongo-uic.git",
    py_modules=["versioned"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)