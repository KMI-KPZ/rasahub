from setuptools import setup, find_packages

setup(
    name='rasahub',
    version='0.0.12',
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
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['rasa-core', 'rasa_nlu', 'mysql-connector==2.1.4'],
    entry_points={
       'console_scripts': [
           'rasahub = rasahub:main',
       ],
    }
)
