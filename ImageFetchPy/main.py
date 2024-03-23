"""
Version 1.2 of ImageFetchPy
--Includes modifications so that it does not downloads images of icons, navbar etc.
--Now saves image url in a text file inside a folder 'url' present inside the folder    which contains images based on the given query name

Author - Sai Smaran Panda

"""



import os
import time
import requests
import urllib
import magic
import progressbar
from urllib.parse import quote

def initialize():
    """
    Placeholder function for any initialization tasks.
    """
    pass

def create_image_directories(directory, name):
    """
    Create directory to save images based on the provided directory path and name.

    :param directory: The main directory path where subdirectories will be created.
    :param name: The name of the subdirectory to be created.
    """
    name = name.replace(" ", "_")
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            time.sleep(0.2)

        sub_directory = os.path.join(directory, name)
        if not os.path.exists(sub_directory):
            os.makedirs(sub_directory)
    except OSError as e:
        if e.errno != 17:  # Ignore "File exists" error
            raise

def download_page(url):
    """
    Download the HTML content of a web page using the provided URL.

    :param url: The URL of the web page to download.
    :return: The HTML content of the web page as a string.
    """
    try:
        headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        return resp.read().decode('utf-8')
    except Exception as e:
        print(e)
        raise

def download_image(url, directory, keyword, extensions, last_number, bar):
    """
    Download a single image from the provided URL and save it to the specified directory.

    :param url: The URL of the image to download.
    :param directory: The directory to save the image.
    :param keyword: The keyword associated with the image.
    :param extensions: Set of valid image file extensions to download.
    :param last_number: The last number used for naming images.
    :param bar: Progress bar to update.
    """
    try:
        if not url.startswith('https://encrypted-tbn0.gstatic.com/'):
            r = requests.get(url, allow_redirects=True, timeout=1)
            if 'html' not in str(r.content):
                mime = magic.Magic(mime=True)
                file_type = mime.from_buffer(r.content)
                file_extension = f'.{file_type.split("/")[1]}'
                if file_extension not in extensions:
                    raise ValueError()

                # Increment image counter and check if it's greater than 3
                file_name = f"{keyword}_{last_number + 1}{file_extension}"
                with open(os.path.join(directory, file_name), 'wb') as file:
                    file.write(r.content)
                    bar.update(bar.currval + 1)
            else:
                raise ValueError("HTML content received instead of image.")
    except Exception as e:
        raise

def download_images_from_html(html_content, directory, keyword, extensions, limit, last_number, bar):
    """
    Download images from the HTML content of a web page and save them to the specified directory.

    :param html_content: The HTML content of the web page containing image links.
    :param directory: The directory to save the images.
    :param keyword: The keyword associated with the images.
    :param extensions: Set of valid image file extensions to download.
    :param limit: Maximum number of images to download.
    :param last_number: The last number used for naming images.
    :param bar: Progress bar to update.
    """
    end_object = -1
    image_counter = 0  # Counter for downloaded images

    while image_counter < limit:
        try:
            new_line = html_content.find('"https://', end_object + 1)
            end_object = html_content.find('"', new_line + 1)

            buffor = html_content.find('\\', new_line + 1, end_object)
            if buffor != -1:
                object_raw = html_content[new_line + 1:buffor]
            else:
                object_raw = html_content[new_line + 1:end_object]

            # Check if the object link contains a valid image extension and exclude unwanted patterns
            if any(extension in object_raw for extension in extensions) and not any(pattern in object_raw for pattern in ['ssl.gstatic.com', 'www.gstatic.com']):
                time.sleep(1)  # Wait for 1 second before downloading the next image
                download_image(object_raw, directory, keyword, extensions, last_number, bar)
                image_counter += 1
                last_number += 1

        except Exception as e:
            pass

'''def download_query(keywords, limit, extensions={'.jpg', '.png', '.ico', '.gif', '.jpeg'}):
    """
    Download images based on user-provided keywords and limits.

    :param keywords: Keywords to search for images (comma-separated if multiple).
    :param limit: Maximum number of images to download per keyword.
    :param extensions: Set of valid image file extensions to download.
    """
    keyword_to_search = [str(item).strip() for item in keywords.split(',')]
    main_directory = "images/"
    total_images = len(keyword_to_search) * limit
    bar = progressbar.ProgressBar(maxval=total_images, widgets=[progressbar.Bar('*', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    for keyword in keyword_to_search:
        create_image_directories(main_directory, keyword)
        url = f'https://www.google.com/search?q={quote(keyword.encode("utf-8"))}&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770&source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ'
        html_content = download_page(url)

        # Check existing images for numbering continuation
        existing_images = os.listdir(os.path.join(main_directory, keyword.replace(" ", "_")))
        existing_numbers = [int(img.split("_")[-1].split(".")[0]) for img in existing_images if img.startswith(keyword)]
        last_number = max(existing_numbers) if existing_numbers else 0

        download_images_from_html(html_content, os.path.join(main_directory, keyword.replace(" ", "_")), keyword, extensions, limit, last_number, bar)

    bar.finish()
    print("Downloading Complete")'''


import os
from urllib.parse import quote

def create_url_directory(directory, name):
    """
    Create a directory to save URL text files based on the provided directory path and name.

    :param directory: The main directory path where subdirectories will be created.
    :param name: The name of the subdirectory to be created.
    """
    try:
        name = name.replace(" ", "_")
        url_directory = os.path.join(directory, name, "url")
        if not os.path.exists(url_directory):
            os.makedirs(url_directory)
    except OSError as e:
        if e.errno != 17:  # Ignore "File exists" error
            raise

def write_urls_to_file(directory, keyword, url):
    """
    Write the URL to a text file inside the URL directory.

    :param directory: The main directory path where subdirectories are located.
    :param keyword: The keyword associated with the URL.
    :param url: The URL to write to the file.
    """
    try:
        name = keyword.replace(" ", "_")
        url_directory = os.path.join(directory, name, "url")
        url_file_path = os.path.join(url_directory, f"{name}_urls.txt")
        with open(url_file_path, 'a') as url_file:
            url_file.write(url + '\n')
    except Exception as e:
        print(e)
        raise

def download_query(keywords, limit, extensions={'.jpg', '.png', '.ico', '.gif', '.jpeg'}):
    """
    Download images based on user-provided keywords and limits.

    :param keywords: Keywords to search for images (comma-separated if multiple).
    :param limit: Maximum number of images to download per keyword.
    :param extensions: Set of valid image file extensions to download.
    """
    keyword_to_search = [str(item).strip() for item in keywords.split(',')]
    main_directory = "images/"

    for keyword in keyword_to_search:
        create_image_directories(main_directory, keyword)
        create_url_directory(main_directory, keyword)
        url = f'https://www.google.com/search?q={quote(keyword.encode("utf-8"))}&tbm=isch'
        html_content = download_page(url)

        existing_images = os.listdir(os.path.join(main_directory, keyword.replace(" ", "_")))
        existing_numbers = [int(img.split("_")[-1].split(".")[0]) for img in existing_images if img.startswith(keyword)]
        last_number = max(existing_numbers) if existing_numbers else 0

        bar = progressbar.ProgressBar(maxval=limit, widgets=[progressbar.Bar('*', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        image_counter = 0
        end_object = -1

        while image_counter < limit:
            try:
                new_line = html_content.find('"https://', end_object + 1)
                end_object = html_content.find('"', new_line + 1)

                buffor = html_content.find('\\', new_line + 1, end_object)
                if buffor != -1:
                    object_raw = html_content[new_line + 1:buffor]
                else:
                    object_raw = html_content[new_line + 1:end_object]

                if any(extension in object_raw for extension in extensions) and not any(pattern in object_raw for pattern in ['ssl.gstatic.com', 'www.gstatic.com']):
                    time.sleep(1)
                    download_image(object_raw, os.path.join(main_directory, keyword.replace(" ", "_")), keyword, extensions, last_number, bar)
                    write_urls_to_file(main_directory, keyword, object_raw)
                    image_counter += 1
                    last_number += 1

            except Exception as e:
                pass

        bar.finish()

    print("Downloading Complete")


download_query("india",10)

