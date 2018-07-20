from setuptools import setup

setup(
    name='boiler',
    version='1.0',
    py_modules=['boiler'],
    install_requires=[
        'Click',
	'jinja2',
    ],
    entry_points='''
        [console_scripts]
        boiler=boiler:render_it
    ''',
)
