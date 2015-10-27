from distutils.core import setup
setup(name='boxmanager',
      version='0.1',
      py_modules=['authenticate', 'box_wrapper', 'cli'],
      install_requires=['boxsdk>=1.2.2',
                        'py>=1.4.30',
                        'pytest>=2.8.2',
                        'PyYAML>=3.11',
                        'requests>=2.8.1',
                        'six>=1.10.0',
                        ]
      )
