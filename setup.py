"""
This file is part of the telex project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Jul 5, 2014.
"""
from setuptools import find_packages
from setuptools import setup

setup(name='telex_rgg',
      version='0.1',
      description='RGG template generation for telex server commands.',
      author='F. Oliver Gathmann',
      author_email='fogathmann at gmail.com',
      license="MIT",
      packages=find_packages(),
      package_data={'': ["*.zcml", "*.mak"]},
      include_package_data=True,
      zip_safe=False,
      install_requires=['telex'],
      entry_points=\
      """
      [telex.plugins]
      telex_rgg = telex_rgg:load_plugin
      """
      )


