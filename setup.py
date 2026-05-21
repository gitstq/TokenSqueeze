#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TokenSqueeze - 轻量级LLM Token智能压缩工具
安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取README
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = ''
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='tokensqueeze',
    version='1.0.0',
    author='TokenSqueeze Team',
    author_email='hello@tokensqueeze.dev',
    description='轻量级LLM Token智能压缩工具 - Lightweight LLM Token Compression Tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gitstq/TokenSqueeze',
    py_modules=['tokensqueeze'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Tools',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    keywords='llm token compression ai claude cursor codex cli tool',
    project_urls={
        'Bug Reports': 'https://github.com/gitstq/TokenSqueeze/issues',
        'Source': 'https://github.com/gitstq/TokenSqueeze',
        'Documentation': 'https://github.com/gitstq/TokenSqueeze#readme',
    },
    entry_points={
        'console_scripts': [
            'tokensqueeze=tokensqueeze:main',
            'tsq=tokensqueeze:main',
        ],
    },
)
