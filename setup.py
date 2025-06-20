from setuptools import setup, find_packages

setup(
    name="django-smartcli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Django>=4.2"],
    author="Nathan Renard",
    description="A smart CLI for Django to help you create and manage your project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nathanrenard/django-smartcli",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
