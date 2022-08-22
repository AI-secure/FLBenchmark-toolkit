from setuptools import setup

setup(
    name='flbenchmark',
    version='0.1.3',
    description='flbenchmark',
    author='stneng',
    author_email='git@stneng.com',
    url='https://github.com/AI-secure/FLBenchmark-toolkit',
    packages=['flbenchmark', 'flbenchmark.datasets', 'flbenchmark.logging'],
    package_dir={'flbenchmark': 'src'},
    install_requires=[
        'pandas>=0.25',
        'numpy>=1.18',
        'scipy',
        'Pillow',
    ],
    python_requires='>=3.6',
)
