from setuptools import setup


setup(
    name='purple-llama',
    version='0.1.0',
    description='A Purple Twitch Enabled Llama2 ',
    url='https://github.com/graylan0/purple-llama',
    author='gray00',
    author_email='graylan0@protonmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='purple llama',
    packages=['purple_llama'],
    install_requires=[
        'llama-cpp-python==0.1.78',
        'twitchio',
        'requests',
        'pydantic',
        'pydantic_settings',
        'fastapi',
        'uvicorn-loguru-integration',
        'uvicorn',                                               
    ],
    extras_require={
        'dev': ['isort', 'blue'],
    },
    entry_points={
        'console_scripts': ['purple_llama=purple_llama.__main__:main'],
    },
)
