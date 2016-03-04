from setuptools import setup, find_packages

VERSION = '0.1'

REQUIREMENTS = (
    'ipaddress==1.0.4',
    'python-dateutil==2.1',
    'requests==2.9.1'
)
TEST_REQUIREMENTS = (
)


setup(
    name="adyengo",
    version=VERSION,
    author="Rik",
    author_email="gitaarik@gmail.com",
    description="Integrate Adyen in Django.",
    long_description=open('README.md', 'rt').read(),
    url="https://github.com/gitaarik/adyengo",
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
