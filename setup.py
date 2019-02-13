from setuptools import setup, find_packages

setup(
    name='autocomplete_api',
    version='0.1.0',
    description='Auto complete service for HOPE',
    url='https://github.com/pypa/sampleproject',
    author='Ali Mosavian',
    author_email='ali@hedvig.com',

    python_requires='>=3.6',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'elasticsearch==6.3.1',
        'elasticsearch-dsl==6.3.1',
        'emoji==0.5.1',
        'connexion[swagger-ui]==2.2.0',
        'gevent==1.4.0',
        'nltk==3.4',
        'pyyaml==4.2b2',
        'certifi==2018.11.29',
        'sqlalchemy==1.2.17',
        'psycopg2-binary==2.7.7'
    ],
    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={
        'auto_complete_api': ['config.yaml', 'api_spec.yaml'],
    },

    entry_points={
        'console_scripts': [
            'run_autocomplete_service=auto_complete_api.main:main',
        ],
    },
)