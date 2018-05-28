from setuptools import setup, find_packages

install_requires = [
    'PyYaml',
]

tests_requires = [
    'rasahub-humhub',
    'rasahub-rasa',
    'rasahub-google-calendar',
    'testing.common.database',
    'testing.mysqld',
    'nltk',
]

extras_requires = {
    'test': tests_requires
}

def get_version():
    version_file = open('../VERSION')
    return version_file.read().strip()

setup(
    name='rasahub',
    version=get_version(),
    description='Rasahub connects Rasa_core to Humhub Mail',
    author='Christian Frommert',
    author_email='christian.frommert@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
    ],
    keywords='humhub rasa rasa_core',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=install_requires,
    tests_require=tests_requires,
    extras_require=extras_requires,
    entry_points={
       'console_scripts': [
           'rasahub = rasahub:main',
       ],
    }
)
