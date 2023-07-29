from setuptools import setup

REQUIRES = [
    "sqlalchemy",
    "structlog",
    "allure-pytest",
]

setup(
    name='orm_client',
    version='0.0.1',
    packages=['orm_client'],
    url='https://github.com/vladgerasimov94/orm_client.git',
    license='MIT',
    author='Vladislav Gerasimov',
    author_email='-',
    install_requires=REQUIRES,
    description='orm client with allure and logger'
)
