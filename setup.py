from setuptools import setup

setup(
    name='PyObjDB',
    version='0.0.2',
    packages=['PyObjDB', 'PyObjDB.helpers', 'PyObjDB.db_functions'],
    install_requires=["dill", "cryptography"],
    url='https://github.com/megaprokoli/python-object-database',
    license='',
    author='megaprokoli',
    author_email='',
    description='A simple database that can store python objects.'
)
