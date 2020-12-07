from setuptools import setup, find_packages

setup(
    name="bokeh_dev_tools",
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "watchdog",
        "bokeh",
        "selenium"
    ]
)
