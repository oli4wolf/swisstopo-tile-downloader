from setuptools import setup, find_packages

setup(
    name='tile-downloader',
    version='0.1.0',
    author='oli4wolf',
    description='A package to download tiles and data for the https://github.com/oli4wolf/flight-helper Project.',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        "aiohttp==3.9.3",
        "pygeotile==1.0.6",
        "pylineclip==1.0.0",
        "Requests==2.31.0"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)