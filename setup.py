#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_workwx
=================================================
"""

import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="py3-workwx",
    version="1.1.6",
    description="The Python3 Work Weixin Library Developed By Guolei",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guolei19850528/py3_workwx",
    author="guolei",
    author_email="174000902@qq.com",
    license="MIT",
    keywors=["workwx", "work weixin", "企业微信", "群机器人", "服务端API", "webhook"],
    packages=setuptools.find_packages('./'),
    install_requires=[
        "py3-requests",
        "addict",
        "retrying",
        "jsonschema",
        "diskcache",
        "redis",
    ],
    python_requires='>=3.0',
    zip_safe=False
)
