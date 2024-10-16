from setuptools import setup, find_packages

setup(
    name='BacPosNeg',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            # Command for genome classification
            'genome_classifier = genome_classifier.scripts.main:main',
            
            # Command for GP/GN ratio calculation
            'ratio_calculator = ratio_calculator.main:main',
        ]
    },
)

