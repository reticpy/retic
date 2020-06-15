import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='retic',
    version='0.0.9',
    license='MIT',
    description='Fastest, easiest and simple web framework for Python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Braian Staimer',
    author_email='braianflorian@gmail.com',
    url='https://github.com/reticpy/retic',
    packages=setuptools.find_packages(),
    include_package_data=True,    
    download_url='https://github.com/reticpy/retic/archive/0.0.9.tar.gz',
    keywords=['PYTHON', 'WEB FRAMEWORK', 'MACHINE LEARNING WEB FRAMEWORK'],
    install_requires=[
        "environs>=7.4.0",
        "httpmethods>=1.0.5",
        "Werkzeug>=1.0.0",
        "repath>=0.9.0"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
