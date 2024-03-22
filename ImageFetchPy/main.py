import os
import time
import requests
import urllib
import magic  # Requires 'python-magic' library
import progressbar  # Requires 'progressbar2' library
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
    # Replace spaces in the name with underscores
    name = name.replace(" ", "_")
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            time.sleep(0.2)
        # Create subdirectory if it doesn't exist
        path = name
        sub_directory = os.path.join(directory, path)
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
        respData = str(resp.read())
        return respData
    except Exception as e:
        print(e)
        exit(0)

def download_query(keywords, limit, extensions={'.jpg', '.png', '.ico', '.gif', '.jpeg'}):
    """
    Download images based on user-provided keywords and limits.

    :param keywords: Keywords to search for images (comma-separated if multiple).
    :param limit: Maximum number of images to download per keyword.
    :param extensions: Set of valid image file extensions to download.
    """
    keyword_to_search = [str(item).strip() for item in keywords.split(',')]
    main_directory = "images/"

    # Calculate the total number of iterations needed for the progress bar
    things = len(keyword_to_search) * limit

    # Initialize progress bar
    bar = progressbar.ProgressBar(maxval=things, \
                                   widgets=[progressbar.Bar('*', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    i = 0
    while i < len(keyword_to_search):
        create_image_directories(main_directory, keyword_to_search[i])
        url = 'https://www.google.com/search?q=' + quote(keyword_to_search[i].encode('utf-8')) + '&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770&source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ'
        raw_html = download_page(url)

        end_object = -1
        google_image_seen = False
        j = 0
        image_counter = 0  # Counter for downloaded images

        # Check existing images for numbering continuation
        existing_images = os.listdir(main_directory + keyword_to_search[i].replace(" ", "_"))
        existing_numbers = [int(img.split("_")[-1].split(".")[0]) for img in existing_images if img.startswith(keyword_to_search[i])]
        if existing_numbers:
            last_number = max(existing_numbers)
        else:
            last_number = 0

        while j < limit + 3:  # Allow for some extra iterations to handle exceptions
            while True:
                try:
                    new_line = raw_html.find('"https://', end_object + 1)
                    end_object = raw_html.find('"', new_line + 1)

                    buffor = raw_html.find('\\', new_line + 1, end_object)
                    if buffor != -1:
                        object_raw = (raw_html[new_line + 1:buffor])
                    else:
                        object_raw = (raw_html[new_line + 1:end_object])

                    # Check if the object link contains a valid image extension
                    if any(extension in object_raw for extension in extensions):
                        break

                except Exception as e:
                    break

            path = main_directory + keyword_to_search[i].replace(" ", "_")

            try:
                r = requests.get(object_raw, allow_redirects=True, timeout=1)
                if ('html' not in str(r.content)):
                    mime = magic.Magic(mime=True)
                    file_type = mime.from_buffer(r.content)
                    file_extension = f'.{file_type.split("/")[1]}'
                    if file_extension not in extensions:
                        raise ValueError()

                    if file_extension == '.png' and not google_image_seen:
                        google_image_seen = True
                        raise ValueError()

                    # Increment image counter and check if it's greater than 3
                    image_counter += 1
                    if image_counter > 3:
                        file_name = f"{keyword_to_search[i]}_{last_number + j + 1 - 3}{file_extension}"
                        with open(os.path.join(path, file_name), 'wb') as file:
                            file.write(r.content)
                        bar.update(bar.currval + 1)

                else:
                    j -= 1  # Retry downloading if encounter HTML content
            except Exception as e:
                j -= 1  # Retry downloading on exception
            j += 1

        i += 1

    bar.finish()
    print("Downloading Complete")


