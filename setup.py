import io

from setuptools import setup, find_packages


def get_long_description():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='AssetVendor',
    version='0.0.1',
    author='Ryan P Kilby',
    url='https://github.com/rpkilby/AssetVendor',
    description='A simple dealer of node packages...',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    license='BSD',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    extras_require={
        'dev': ['tox', 'tox-venv', 'ipython'],
        'packaging': ['packaging'],
        'yaml': ['pyyaml'],
    },
    entry_points={
        'console_scripts': [
            'vendor = assetvendor.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
