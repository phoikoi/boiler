from setuptools import setup

setup(
    name='boiler',
    version='1.2',
    py_modules=['boiler'],
    install_requires=[
        'Click',
	'jinja2',
    ],
    entry_points='''
        [console_scripts]
        boiler=boiler:render_it
    ''',
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',
    ]
)
