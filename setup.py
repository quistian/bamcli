from setuptools import setup

setup(
        name='BAM CLI Interface',
        version='0.0.1',
        author='Russell Sutherland'
        author_email='russell.sutherland@utoronto.ca'
        description='A Command Line Interface using the BAM Python API to manage DNS data"
        py_modules=[
            'requests',
            'Click',
        ],
        entry_points='''
            [console_scripts]
            bamcli=bamcli:cli
        ''',
)
