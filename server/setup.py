#!/usr/bin/env python

from setuptools import setup

setup(name='haste_image_pipeline_server',
      version='0.10',
      packages=['haste.k8.worker'],
      namespace_packages=[
          'haste',
          'haste.k8'
      ],
      author='Ben Blamey',
      author_email='ben.blamey@it.uu.se',
      install_requires=[
          'pika'
      ],
      test_requires=[
          'pytest'
      ]
      )
