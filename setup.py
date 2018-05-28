from setuptools import setup, find_packages

__version__ = None
exec(open("rasahub/version.py").read())

install_requires = [
    'PyYaml',
]

tests_requires = [
]

extras_requires = {
    'test': tests_requires
}

setup(
    name='rasahub',
    version=__version__,
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
