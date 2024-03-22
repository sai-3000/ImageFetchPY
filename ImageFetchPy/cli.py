import argparse
from .main import download_query

def main():
    parser = argparse.ArgumentParser(description='ImageFetchPy CLI')
    parser.add_argument('keywords', type=str, help='Keywords to search for images (comma-separated if multiple)')
    parser.add_argument('--limit', type=int, default=10, help='Maximum number of images to download per keyword (default: 10)')
    args = parser.parse_args()

    keywords = args.keywords
    limit = args.limit

    download_query(keywords, limit)

if __name__ == '__main__':
    main()
