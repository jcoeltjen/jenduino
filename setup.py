from setuptools import setup, find_packages
from codecs import open


def load_readme():
    with open('README.md', encoding='utf-8') as file:
        return file.read()


def requirements(filename):
    dependencies = []
    with open(filename, encoding='utf-8') as file:
        for line in file.readlines():
            if not line.strip().startswith('#'):
                dependencies.append(line.strip())

        return dependencies


setup(
    name='jenduino',
    version='0.1.dev0',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/jcoeltjen/jenduino',
    license='MIT',
    author='Jannis Oeltjen',
    author_email='oss@jcoeltjen.de',
    description='Jenduiono python server.',
    long_description=load_readme(),
    install_requires=requirements('requirements.txt'),
    setup_requires=requirements('requirements_dev.txt'),
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'jenduino = jenduino.entrypoint:start'
        ]
    }
)
