from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


# Parse the version from the fiona/rasterio module.
with open('usgs/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue


setup(name='usgs',
      version=version,
      description=u"Access the USGS inventory service",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Amit Kapadia",
      author_email='amit@planet.com',
      url='https://github.com/kapadia/usgs',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      package_data={'usgs': ['data/datasets.json']},
      zip_safe=False,
      install_requires=[
          'click>=4.0',
          'requests>=2.7.0',
          'requests_futures>=0.9.5'
      ],
      extras_require={
          'test': ['pytest', 'mock'],
      },
      entry_points="""
      [console_scripts]
      usgs=usgs.scripts.cli:usgs
      """
      )