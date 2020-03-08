# SteemYaLater
A Python Script that uses the Steem Beem Library and a variety of methods to Archive your Steem Blockchain  Blog Markdown as Text Files and Backs up Images

# Version 2.0 Change Notes

- Added PyCurl download method to address issues w steemitboard images
- Data Deplication enabled: Prevents redownload of file if already exists in folder structure. Symbolic link with relative path placed instead saving valuable storage space.
- Logging and CSV output: Session log file is produced in working directory. Output CSVs are created for each account so users may readily see what failed and may require manual action. 

# Known Issues

DTube thumbnails will not download as they are not stored within the Beem Comment json_metadata image property. Logic to be added to accomodate.

Uses Python 3.6

# PyCurl may require the following packages be installed.

sudo apt install libcurl4-openssl-dev libssl-dev

# Install Prerequisites
Python 3.6 -m pip install beem
Python 3.6 -m pip install wget
Python 3.6 -m pip install urllib3[secure]
Python 3.6 -m pip install pycurl
Python 3.6 -m pip install certifi #may or may not be needed if the [secure] option is used for urllib3

# Execute Script

python3.6 SteemYaLater.py

# Prompts for Steem User. Alternatively, you may populate the accounts list variable with users to backup

Account to Backup? anthonyadavisii

# Script will crawl your blog_entries filtering out resteems (reblogs)

![st4y66.png](https://img.esteem.app/st4y66.png)

# Will then cycle through each blog_entry, save the body to a .txt files, and grab any images it can with wget or urllib3
