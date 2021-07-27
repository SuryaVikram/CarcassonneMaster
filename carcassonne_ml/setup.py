from setuptools import setup, find_namespace_packages

setup(name='wingedsheep-carcassonne-ml',
      version='1.0.0',
      description='Carcassonne machine learning implementation',
      author='Vincent Bons',
      url='https://github.com/wingedsheep/carcassonne-ml',
      download_url='https://github.com/wingedsheep/carcassonne-ml',
      license='MIT',
      dependency_links=['https://github.com/wingedsheep/carcassonne/tarball/a1d9987ba077e8abba3e7532285db6d194f62a87'],
      packages=find_namespace_packages())
