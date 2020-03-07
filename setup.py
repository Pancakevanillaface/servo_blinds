from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="autoblinds", # Replace with your own username
    version="0.0.1",
    author="pancakevanillaface",
    description="Python-based process to automate servos based on sunrise/sunset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pancakevanillaface/autoblinds",
    packages=find_packages(),
    python_requires='==3.7.5',
    py_modules=['autoblinds'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        autoblinds=autoblinds.cli:cli
    ''',
)