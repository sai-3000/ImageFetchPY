from setuptools import setup, find_packages

setup(
    name='ImageFetchPy',
    version='1.0.2',
    author='Sai Smaran Panda',
    author_email='smaran06ncn@gmail.com',
    description='A library for scraping and downloading images from the web.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'python-magic-bin==0.4.14',
        'progressbar2',
        'urllib3',
        'requests',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'imagefetch = ImageFetchPy.cli:main',  
        ],
    },
    url='https://github.com/sai-3000/ImageFetchPY',
    project_urls={
        'Source': 'https://github.com/sai-3000/ImageFetchPY',
        'Tracker': 'https://github.com/sai-3000/ImageFetchPY',
    },
)
