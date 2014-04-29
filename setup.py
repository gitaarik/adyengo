from setuptools import setup, find_packages

VERSION = '0.1'

REQUIREMENTS = (
    'ipaddress==1.0.4',
    'python-dateutil==2.1',
    'suds==0.4',
)
TEST_REQUIREMENTS = (
)


setup(
    name="adyengo",
    version=VERSION,
    author="Rik, Douwe van der Meij",
    author_email="gitaarik@gmail.com, vandermeij@gw20e.com",
    description="""Integrate Adyen in Django.
    """,
    long_description=open('README.md', 'rt').read(),
    url="https://github.com/Goldmund-Wyldebeast-Wunderliebe/adyengo",
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
