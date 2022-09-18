from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='http_status_service',
    version='0.1.0',
    description='HTTP status service',
    long_description=readme,
    author='Lazaros Kazantzis',
    author_email='lazaros.kazantzis@gmail.com',
    url='https://github.com/larry482gr/http_status_service',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'requests>=2.28.1',
        'prometheus-client>=0.14.1'
    ]
)
