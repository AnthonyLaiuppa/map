from setuptools import setup, find_packages
setup(
    name='map',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Requests',
        'beautifulsoup4'
    ],
    entry_points='''
        [console_scripts]
        map=map:start_mapping
    ''',
)
