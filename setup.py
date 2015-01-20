from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='usgs',
      version='0.1.0',
      description=u"Access the USGS inventory service",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Amit Kapadia",
      author_email='amit@mapbox.com',
      url='https://github.com/mapbox/usgs',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      package_data={'usgs': ['data/datasets.json']},
      zip_safe=False,
      install_requires=['click', 'requests'],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      usgs=usgs.scripts.cli:usgs
      """
      )
