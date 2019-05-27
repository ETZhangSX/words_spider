from setuptools import setup, find_packages

setup(
    name='words',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = words.settings']},
    include_package_data=True,
    url='',
    license='',
    author='et',
    author_email='etzhangsx@qq.com',
)
