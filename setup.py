from setuptools import setup, find_packages


setup(
    name='adyengo',
    keywords='django adyen payment integration',
    version='0.0.10',
    author='gitaarik',
    author_email='gitaarik@gmail.com',
    description='Django app for easy Adyen integration.',
    url='https://github.com/gitaarik/adyengo',
    license='LGPL licence, see LICENCE.txt',
    packages=find_packages(),
    include_package_data=True,
    install_requires=('ipaddress', 'python-dateutil', 'requests'),
    zip_safe=False,
)
