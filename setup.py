from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="servo-blinds",
    version="0.0.1",
    author="pancakevanillaface",
    description="Python-based tool to control servos via mqtt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pancakevanillaface/servo_blinds",
    packages=find_packages(),
    python_requires='>=3.9',
    py_modules=['servo-blinds'],
    install_requires=[
        'PyYAML',
        'adafruit-circuitpython-servokit',
        'adafruit-circuitpython-vcnl4040',
        'paho-mqtt',
        'coverage',
        'pytest',
        'pytest-mock'
    ]
)
