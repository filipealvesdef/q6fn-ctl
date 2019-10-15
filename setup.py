from setuptools import setup

setup(
    name='q6fn-ctl',
    description='Python Controller API for Q6FN Samsung Samrt TV',
    version='1.0.0',
    packages=[
        'q6fn_ctl',
    ],
    install_requires=[
        'wakeonlan~=1.1.6',
        'asyncio~=3.4.3',
    ],
)
