from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


with open("VERSION.md", "r", encoding="utf-8") as version_file:
    sdzkpversion = version_file.read()

setup(
  # TODO: Fix the configs in this part
  name='SDZKP',
  version=sdzkpversion,
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