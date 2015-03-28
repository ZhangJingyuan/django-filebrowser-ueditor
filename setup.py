
import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-filebrowser-ueditor',
    version='1.0',
    description='DjangoUeditor integrates django-filebrowser as image & file manager',
    long_description=README,
    author = 'Zhang Jingyuan',
    author_email = 'jason.jingyuan.zhang@gmail.com',
    
    url='http://www.steppy.co/',
    license='Other/Proprietary License',

    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 5 - Production/Stable',

    # Indicate who your project is intended for
    'Intended Audience :: Customer Service',
    'Topic :: Software Development :: Build Tools',
    'Natural Language :: Chinese (Simplified)'

    # Pick your license as you wish (should match "license" above)
    'License :: Other/Proprietary License',
    'Programming Language :: Python :: 2.7',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],

    packages=['filebrowser_ueditor'],
    include_package_data=True,

    install_requires=[]

)