"""Package configuration."""
import setuptools

setuptools.setup(
    author="Jonathan Bowman",
    description="List and process image tags in a repository in a Docker v2 registry.",
    entry_points={"console_scripts": ["dockertaglist=dockertaglist:run"]},
    name="dockertaglist",
    py_modules=["dockertaglist"],
    version="0.1.0",
)
