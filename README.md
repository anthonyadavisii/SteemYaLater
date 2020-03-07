# SteemYaLater
A Python Script that uses the Steem Beem Library and PyWebCopy to Archive your Steem Blockchain  Blog Markdown as Text Files and Backs up Images

Use Python 3.6

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
