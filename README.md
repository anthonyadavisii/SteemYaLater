# SteemYaLater
A Python Script that uses the Steem Beem Library and PyWebCopy to Archive your Steem Blockchain  Blog Markdown as Text Files and Backs up Images

Use Python 3.6

# Install Prerequisites
Python 3.6 -m pip install beem
Python 3.6 -m pip install wget
Python 3.6 -m pip install urllib3[secure]

# Execute Script

python3.6 SteemYaLater.py

# Prompts for Steem User

Account to Backup? anthonyadavisii

# Script will crawl your blog_entries filtering out resteems (reblogs)

![st4y66.png](https://img.esteem.app/st4y66.png)

# Will then cycle through each blog_entry, save the body to a .txt files, and grab any images it can with wget or urllib3
