from setuptools import setup

setup(
        name='BAM CLI Interface',
        version='0.0.1',
        description='Python Command Line Interface to BAM',
        author='Russell Sutherland',
        author_email='russell.sutherland@utoronto.ca',
        py_modules=[
            'requests',
            'Click',
        ],
        entry_points='''
            [console_scripts]
            bamcli=bamcli:cli
        ''',
)
