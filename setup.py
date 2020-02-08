import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='chain-norm',
    version='0.0.1',
    author='Ryota Yamada',
    author_email='roy29fuku@gmail.com',
    description='chain-norm is python library for suquential text normalization',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/roy29fuku/chain-norm',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
    ],
    python_requires='>=3.8',
)
