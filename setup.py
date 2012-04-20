from distutils.core import setup

setup(
    name='translatePyoptNLPy',
    version='0.1',
    author='Sylvain Arreckx',
    author_email='sylvain.arreckx@gmail.com',
    packages=['translatePyoptNLPy'],
    scripts=[],
    description='Translation package between pyOpt and NLPy.',
    long_description=open('README.txt').read(),
    install_requires=[
        "nlpy >= 0.2",
        "pyopt >= 1.0",
    ],
)
