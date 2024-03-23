# ImageFetchPy
ImageFetchPy is a Python library designed to simplify the process of scraping and downloading images from the web, specifically targeting Google Image Search based on user-provided keywords.

## Features
- Download images from Google Image Search using keywords.
- Specify the maximum number of images to download per keyword.
- Support for various image file extensions such as jpg, png, gif, etc.
- Enhanced filtering to exclude downloading images of icons, navbars, etc.
- Save image URLs in a text file for easy reference and management.
- Skips downloading duplicate images based on URL comparison.- 

## Version 1.2
Version 1.2 includes modifications:
- Includes modifications so that it does not downloads images of icons, navbar etc.
- Now saves image url in a text file inside a folder 'url' present inside the folder    which contains images based on the given query name


## Installation
You can install ImageFetchPy using pip:

```bash
pip install ImageFetchPy
```


## Usage
### Using the Library in a Python Script
Import the 'download_query' function from ImageFetchPy and use it to download images:
```python
from ImageFetchPy import download_query

# Download images based on keywords
download_query("cat, dog, bird", limit=10)
```

### Using the Command-Line Interface (CLI)
ImageFetchPy provides a command-line interface for convenient usage:
```bash
imagefetch "cat, dog, bird" --limit 10
```


## Parameters
- keywords: Keywords to search for images (comma-separated if multiple).
- limit: Maximum number of images to download per keyword.
- extensions: Set of valid image file extensions to download (default: {'jpg', 'png', 'ico', 'gif', 'jpeg'}).


## Version 1.2 Changes
In version 1.2, ImageFetchPy introduces the following improvements:

- Exclude downloading images of icons, navbars, and similar elements.
- Save image URLs in a structured format inside a 'url' folder for each keyword query.
- Skips downloading duplicate images based on URL comparison.






