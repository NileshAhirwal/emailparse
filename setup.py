from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in emailparse/__init__.py
from emailparse import __version__ as version

setup(
	name="emailparse",
	version=version,
	description="This app is use to parse the email content",
	author="Vikram Kumar",
	author_email="alert@onehash.ai",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
