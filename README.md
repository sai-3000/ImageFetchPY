# ImageFetchPy

ImageFetchPy is a Python library for scraping and downloading images from the web based on user-provided keywords.

## Features

- Download images from Google Image Search based on keywords.
- Specify the maximum number of images to download per keyword.
- Supports various image file extensions like jpg, png, gif, etc.
- Includes a command-line interface (CLI) for easy usage.


## Version 1.2
Version 1.2 includes modifications:
- Includes modifications so that it does not downloads images of icons, navbar etc.
- Now saves image url in a text file inside a folder 'url' present inside the folder    which contains images based on the given query name



## Installation

You can install ImageFetchPy using pip:

```bash
pip install ImageFetchPy

Usage
Using the Library in a Python File

from ImageFetchPy import download_query

# Download images based on keywords
download_query("cat, dog, bird",10)


Using the Command Line Interface (CLI)

imagefetch  "cat, dog, bird" --limit 10



Parameters
--keywords: Keywords to search for images (comma-separated if multiple).
--limit: Maximum number of images to download per keyword.
--extensions: Set of valid image file extensions to download (default: {'jpg', 'png', 'ico', 'gif', 'jpeg'}).