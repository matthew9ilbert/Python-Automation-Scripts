#!/usr/bin/env python

import sys
import os
import hashlib
import logging
import urllib.request

def get_hash(file_name):
    """Generate MD5 hash for the first and last 64kb of the video file."""
    read_size = 64 * 1024
    with open(file_name, 'rb') as file:
        size = os.path.getsize(file_name)
        data = file.read(read_size)
        file.seek(-read_size, os.SEEK_END)
        data += file.read(read_size)
    return hashlib.md5(data).hexdigest()

def download_subtitle_enhanced(file_path):
    """Download subtitles for a given video file."""
    try:
        base_name, ext = os.path.splitext(file_path)
        valid_extensions = [".avi", ".mp4", ".mkv", ".mpg", ".mpeg", ".mov", ".rm", ".vob", ".wmv", ".flv", ".3gp", ".3g2"]
        
        if ext not in valid_extensions:
            logging.info(f'{ext} is not a valid video format.')
            return

        subtitle_name = base_name + '.srt'
        if not os.path.exists(subtitle_name):
            headers = {
                'User-Agent': 'SubDB/1.0 (subtitle-download/1.0; https://github.com/shan18/Python-Automation-Scripts/)'
            }
            url = f'http://api.thesubdb.com/?action=download&hash={get_hash(file_path)}&language=en'
            req = urllib.request.Request(url, None, headers)
            content = urllib.request.urlopen(req).read()

            with open(subtitle_name, 'wb') as subtitle_file:
                subtitle_file.write(content)
                logging.info(f'Downloaded subtitle for {base_name} successfully.')
        else:
            logging.info(f'Subtitle for {base_name} already exists.')
    except Exception as e:
        file_name = os.path.basename(file_path)
        logging.error(f'Cannot find subtitles for {file_name}. Error: {e}')

def main():
    """Main function to handle command line arguments and process each file."""
    script_name, _ = os.path.splitext(sys.argv[0])
    logging.basicConfig(filename=f'{script_name}.log', level=logging.INFO)
    logging.info("Parameters given: " + str(sys.argv))

    if len(sys.argv) < 2:
        print('At least one parameter is required.')
        sys.exit(1)

    for path in sys.argv[1:]:
        if os.path.isdir(path):
            for dirpath, _, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    download_subtitle_enhanced(file_path)
        else:
            download_subtitle_enhanced(path)

if __name__ == "__main__":
    main()