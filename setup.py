from setuptools import setup, find_packages
from distutils.util import convert_path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

main_ns = {}
ver_path = convert_path("sdzkp/_version.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
  name='SDZKP',
  version=main_ns['__version__'],
  description="SDZKP: A zero-knowledge proof using subgroup distance problem",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/cansubetin/sdzkp',
  author='Cansu Betin Onur',
  author_email='cansubetin@gmail.com',
  license='GPL V3',
  packages=find_packages(),
  project_urls={
        "Bug Tracker": "https://github.com/cansubetin/sdzkp/issues",
        "Simulator Website": "https://github.com/cansubetin/sdzkp"
  },
  classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
  python_requires=">=3.12",
)