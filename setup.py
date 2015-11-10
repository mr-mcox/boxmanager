from setuptools import setup, find_packages
setup(name='boxmanager',
      version='0.4.3',
      packages=find_packages(exclude=['docs', 'tests']),
      install_requires=['boxsdk>=1.2.2',
                        'et-xmlfile>=1.0.1',
                        'jdcal>=1.0.1',
                        'numpy>=1.10.1',
                        'openpyxl>=2.3.0',
                        'pandas>=0.17.0',
                        'py>=1.4.30',
                        'pytest>=2.8.2',
                        'python-dateutil>=2.4.2',
                        'pytz>=2015.7',
                        'PyYAML>=3.11',
                        'requests>=2.8.1',
                        'six>=1.10.0',
                        'xlrd>=0.9.4',
                        ],
      author="Matthew Cox",
      author_email="matthew.cox@teachforamerica.org",
      )
