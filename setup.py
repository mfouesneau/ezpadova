from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name = "ezpadova",
    version = 1.0,
    description = "A python package that allows you to download PADOVA/PARSEC isochrones directly from their website",
    long_description = readme(),
    author = "Morgan Fouesneau",
    author_email = "",
    url = "https://github.com/mfouesneau/ezpadova",
    packages = find_packages(),
    package_data = {'ezpadova':['*.json']},
    include_package_data = True,
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Science/Research',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Astronomy'
      ],
    zip_safe=False
)
